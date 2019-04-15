# -*- coding: utf-8 -*-
"""SearchES Class to handle searching with ElasticSearch

Authors: Brandon Fan
Last Edit Date: 1/15/2018
"""

import json
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import Q
from fuzzywuzzy import fuzz
import re


class SearchES(object):
    """Class to search using ElasticSearch"
    Attributes:
        client (ElasticSearch): ElasticSearch client object.
    """

    def __init__(self):
        """initializes elasticsearch instance (note: must have ES instance running on localhost:9200)"""
        self.client = Elasticsearch()

    def search(self, term, sort_type='relevant'):

        search_drug = Search(using=self.client, index='drugaid-index')
        query_string = Q(
            'query_string', query=term)
        response = search_drug.query(query_string).highlight('name', 'description', 'generic_names')[
            0: 15].execute()

        final_response = []
        for hit in response.hits.hits:
            data = hit['_source']
            try:
                data['name'] = hit['highlight']['name'][0]
            except KeyError:
                pass

            try:
                data['description'] = hit['highlight']['description'][0]
            except KeyError:
                pass
            try:
                data['generic_names'] = hit['highlight']['generic_names']
            except KeyError:
                pass
            data['score'] = str(hit['_score'])
            final_response.append(data)
        return final_response

    def get_drug(self, search_name):

        search_drug = Search(using=self.client, index='drugaid-index')
        query_string = Q(
            'match', search_name=search_name)
        response = search_drug.query(query_string)[0:1].execute()

        final_response = []
        for hit in response.hits.hits:
            data = hit['_source']
            data['score'] = str(hit['_score'])
            final_response.append(data)
        return final_response[0]


if __name__ == '__main__':
    TEST_SEARCH = SearchES()
    TEST_RESPONSE = TEST_SEARCH.search('janumet')
    print(len(TEST_RESPONSE))
