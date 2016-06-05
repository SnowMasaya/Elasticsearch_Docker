#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import json
import codecs

sys.path.append('.')


class ElasticSearchEngine(object):
    """
    Regist the Document into the Elastic Search
    Reference
      https://elasticsearch-py.readthedocs.org/en/master/
    """

    def __init__(self):
        """
        param: doc_dict: input the doc_dict(document formatting)
        param: config_dict: input the config_dict(document formatting)
        """
        self.es = Elasticsearch()
        self.doc = {}
        self.elastic_index = ""
        self.search_result = []
        self.actions = []

    def regist_data(self, json_file, index=0, bulk_flag=False):
        """
        registing data into the elastic search
        :param json_file(str): regist the index
        :param index(int): regist the id
        :param bulk_flag(boolean): choose using the bulk
        """
        self.json_file = json_file
        f = codecs.open(self.json_file , "r", "utf-8")
        json_data = json.load(f)
        split_json = self.json_file.split("/")
        self.elastic_index = split_json[len(split_json) - 1].replace(".json_tmp.json", "")
        for k, v in json_data.items():
            self.doc.update({k: v})
        res = self.es.index(index=self.elastic_index, doc_type='ja', id=index, body=self.doc)
        res['created']
        f.close()

    def search_data(self, search_key_word):
        """
        search data into the elastic search
        param: search_keyword: you set the search key word
        """
        self.setting_search_query(search_key_word)
        self.res = self.es.search(index=self.elastic_index, body=self.query)
        print("Got %d Hits:" % self.res['hits']['total'])
        for hit in self.res['hits']['hits']:
            print(hit["_source"])
            self.search_result.append(hit["_source"])

    def setting_search_query(self, search_key_word):
        """
        transform the seach key word into the query
        param: search_keyword: you set the search key word
        """
        self.query = {
            "query": {
                "match": {
                    "title": "\"" + search_key_word + "\""
                }
            }
        }