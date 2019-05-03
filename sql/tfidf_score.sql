-- TFIDF SCORE CALCULATION QUERY --
-- Compute TF-IDF score for each token --

SELECT 
  tf_data.song_id,
  tf_data.token, 
  LOG((SELECT COUNT(*) FROM song) / df_data.df) * tf_data.count AS score
FROM token tf_data
LEFT JOIN (
  SELECT 
    token, 
    COUNT(song_id) AS df
  FROM token 
  GROUP BY token
) df_data
ON df_data.token = tf_data.token

-- TFIDF SCORE CALCULATION QUERY END --


-- COPY COMMAND --
-- run this command in psql to copy query output to a csv file
-- then can run \i schema.sql and \i load.sql
-- needs to be all in one line

\copy (SELECT tf_data.song_id, tf_data.token, LOG((SELECT COUNT(*) FROM song) / df_data.df) * tf_data.count AS score FROM token tf_data LEFT JOIN (SELECT token, COUNT(song_id) AS df FROM token GROUP BY token ) df_data ON df_data.token = tf_data.token) TO '/home/cs143/data/tfidf.csv' WITH CSV DELIMITER ',';

-- COPY COMMAND END --


-- OR --

SELECT
  s.song_id,
  SUM(tfidf_scores.score) AS total_score,
  s.artist_id,
  s.song_name,
  s.page_link
FROM (
  SELECT song_id, token, score
  FROM tfidf
  WHERE token IN ('southern', 'california')-- enumerate the words here --
) tfidf_scores
LEFT JOIN song s
ON s.song_id = tfidf_scores.song_id
GROUP BY s.song_id
ORDER BY total_score DESC

-- OR QUERY END --


-- AND -- 

SELECT
  s.song_id,
  SUM(tfidf_scores.score) AS total_score,
  s.artist_id,
  s.song_name,
  s.page_link
FROM (
  SELECT l.song_id, l.token, l.score, r.ref_count
  FROM tfidf AS l
  LEFT JOIN (
    SELECT song_id, COUNT(song_id) AS ref_count
    FROM tfidf
    WHERE token IN  ('party', 'in', 'the', 'u.s.a')
    GROUP BY song_id
  ) r
  ON r.song_id = l.song_id
  WHERE token IN ('party', 'in', 'the', 'u.s.a') AND ref_count = 4
  -- ref_count is the # of unique words searched for --
  -- we're basically making sure the # of times that
  -- song came up in the or clause matches the # of
  -- unique words searched for. if so, we have an AND match,
  -- otherwise that song id is missing 1 or more of the words searched.
) tfidf_scores
LEFT JOIN song s
ON s.song_id = tfidf_scores.song_id
GROUP BY s.song_id
ORDER BY total_score DESC

-- AND QUERY END --


-- playground for building up subqueries --

-- SELECT l.song_id, l.token, l.score, r.ref_count
-- FROM tfidf AS l
-- LEFT JOIN (
--   SELECT song_id, COUNT(song_id) AS ref_count
--   FROM tfidf
--   WHERE token IN ('clockworktime','anne')
--   GROUP BY song_id
-- ) r
-- ON r.song_id = l.song_id
-- WHERE token IN ('clockworktime','anne') AND ref_count = 2
