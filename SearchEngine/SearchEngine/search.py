#!/usr/bin/python3

import psycopg2
import re
import string
import sys

from connect import connect

_PUNCTUATION = frozenset(string.punctuation)

def _remove_punc(token):
    """Removes punctuation from start/end of token."""
    i = 0
    j = len(token) - 1
    idone = False
    jdone = False
    while i <= j and not (idone and jdone):
        if token[i] in _PUNCTUATION and not idone:
            i += 1
        else:
            idone = True
        if token[j] in _PUNCTUATION and not jdone:
            j -= 1
        else:
            jdone = True
    return "" if i > j else token[i:(j+1)]

def _get_tokens(query):
    rewritten_query = []
    tokens = re.split('[ \n\r]+', query)
    for token in tokens:
        cleaned_token = _remove_punc(token)
        if cleaned_token:
            if "'" in cleaned_token:
                cleaned_token = cleaned_token.replace("'", "''")
            rewritten_query.append(cleaned_token)
    return rewritten_query

def search(query, query_type, page):
    """TODO
    Your code will go here. Refer to the specification for projects 1A and 1B.
    But your code should do the following:
    DONE            Connect to the Postgres database.
    SOMEWHAT DONE   Graciously handle any errors that may occur (look into try/except/finally).
    DONE            Close any database connections when you're done.
    4. Write queries so that they are not vulnerable to SQL injections.
    5. The parameters passed to the search function may need to be changed for 1B. 
    """

    rewritten_query = tuple(_get_tokens(query))
    rows = []

    try:
        """TODO
            make this all dynamic, this is just here as a test to make sure that
            it successfully connects to the database

            -- put connection into its own module to clean it up
        """
        drop_materialized_view = """DROP MATERIALIZED VIEW IF EXISTS search_results"""

        query_or = """CREATE MATERIALIZED VIEW search_results AS
            SELECT
            s.song_name,
            a.artist_name,
            s.page_link
            FROM (
            SELECT song_id, token, score
            FROM tfidf
            WHERE token IN %s
            ) tfidf_scores
            LEFT JOIN song s
            ON s.song_id = tfidf_scores.song_id
            LEFT JOIN artist a
            ON a.artist_id = s.artist_id
            GROUP BY s.song_name, a.artist_name, s.page_link
            ORDER BY SUM(tfidf_scores.score) DESC"""

        query_and = """CREATE MATERIALIZED VIEW search_results AS
            SELECT
            s.song_name,
            a.artist_name,
            s.page_link
            FROM (
            SELECT l.song_id, l.token, l.score, r.ref_count
            FROM tfidf AS l
            LEFT JOIN (
                SELECT song_id, COUNT(song_id) AS ref_count
                FROM tfidf
                WHERE token IN %s
                GROUP BY song_id
            ) r
            ON r.song_id = l.song_id
            WHERE token IN %s AND ref_count = %s
            -- ref_count is the # of unique words searched for --
            -- we're basically making sure the # of times that
            -- song came up in the or clause matches the # of
            -- unique words searched for. if so, we have an AND match,
            -- otherwise that song id is missing 1 or more of the words searched.
            ) tfidf_scores
            LEFT JOIN song s
            ON s.song_id = tfidf_scores.song_id
            LEFT JOIN artist a
            ON a.artist_id = s.artist_id
            GROUP BY s.song_name, a.artist_name, s.page_link
            ORDER BY SUM(tfidf_scores.score) DESC"""

        query_page = """SELECT *
            FROM search_results
            LIMIT 20
            OFFSET %s"""

        connection = psycopg2.connect(user = "cs143",
                                    password = "cs143",
                                    host = "localhost",
                                    database = "searchengine")
        cursor = connection.cursor()
        if page < 0:
            cursor.execute(drop_materialized_view)
            if query_type == 'or':
                cursor.execute(query_or, (rewritten_query,))
            else:
                cursor.execute(query_and, (rewritten_query, rewritten_query, len(rewritten_query)))
            cursor.execute(query_page, (0,))
            rows = cursor.fetchall()
            connection.commit()
            page = 0
        else:
            cursor.execute(query_page, (20 * page,))
            rows = cursor.fetchall()

    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL:", error)
        """TODO: Return something meaningful here """

    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

    return (page, rows)

if __name__ == "__main__":
    if len(sys.argv) > 2:
        result = search(' '.join(sys.argv[2:]), sys.argv[1].lower(), 0)
        print(result)
    else:
        print("USAGE: python3 search.py [or|and] term1 term2 ...")

