"""Server to run bible python API

Authors: Brandon Fan, Jordan Seiler
Last Edit Date: 1/15/2018
"""

import uuid
import os
import json
from flask import Flask, request, jsonify, Response
from es_functions import SearchES

APP = Flask(__name__)
print('Initializing Elastic Search Class')
ELASTICSEARCH = SearchES()


@APP.route('/search')
def search_drug_db():
    """Route to search for phrase or term in bible from /search route

    Takes `term` parameter from /search route, and utilizes ElasticSearch to
    to search drug database for associated verse data

    Returns:
        (dict): response dictionary of requested data
        response is below::

            {
                'results': (list),
                'term': (str),
                'search_id': (str),
                'url': (str)
            }

    """
    search_id = str(uuid.uuid4())
    response = {'search_id': search_id, 'url': request.url}
    term = request.args.get('term')
    try:
        sort_type = request.args.get('sort_type')
    except Exception:
        sort_type = 'relevant'
    response['term'] = term
    results = ELASTICSEARCH.search(term, sort_type)
    response['results'] = results
    resp = Response(json.dumps(response), status=200,
                    mimetype='application/json')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@APP.route('/drug')
def get_drug():
    search_id = str(uuid.uuid4())
    response = {'search_id': search_id, 'url': request.url}
    search_name = request.args.get('search_name')
    response['search_name'] = search_name
    result = [ELASTICSEARCH.get_drug(search_name)]
    response['result'] = result
    resp = Response(json.dumps(response), status=200,
                    mimetype='application/json')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


if __name__ == '__main__':
    print('Initializing Server...')
    PORT = int(os.environ.get("PORT", 5000))
    APP.run(host='0.0.0.0', port=PORT)
