#!/usr/bin/python3

from flask import Flask, render_template, request

import search

application = app = Flask(__name__)
app.debug = True

@app.route('/search', methods=["GET"])
def dosearch():
    """
    TODO:
    Use request.args to extract other information
    you may need for pagination.
    """

    pageNum = request.args.get('page', -1)
    query = request.args['query']
    qtype = request.args['query_type']
    pageNum = int(pageNum)

    search_results = search.search(query, qtype, pageNum)

    pageNum = search_results[0]
    rows = search_results[1]

    return render_template('results.html',
            query=query,
            query_type=qtype,
            results=len(rows),
            search_results=rows,
            page=pageNum)


@app.route("/")
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
