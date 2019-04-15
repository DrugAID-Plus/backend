# -*- coding: utf-8 -*-
"""Script to create index of drug database for ElasticSearch (DrugAID+)

Authors: Brandon Fan
Last Edit Date: 2/9/2019
"""
import json
from elasticsearch import Elasticsearch


def create_index():
    """creates index of bible verses for elasticsearch"""
    es = Elasticsearch()
    es.indices.delete(index='drugaid-index')
    with open('../data_crawling/demo_drug_data-fixed.json') as f:
        drug_data = json.load(f)

    for drug in drug_data:
        es.index(index='drugaid-index', doc_type='drug', body=drug)


if __name__ == '__main__':
    create_index()
