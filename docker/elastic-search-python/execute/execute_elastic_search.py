#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import argparse
import pstats,cProfile
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from elastic_search_engine import ElasticSearchEngine
from os import path
APP_ROOT = path.dirname(path.abspath( __file__ ))

"""
This script for execute the elastic search
"""


if __name__ == '__main__':
    """
    args
       -j: crawling json data
           Example: ../data/*.json"
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--json_file', '-j', default='',
                        help='set crawling split data json file')
    parser.add_argument('--index', '-i', default='',
                        help='set index')
    args = parser.parse_args()
    elastic_search = ElasticSearchEngine()
    elastic_search.regist_data(args.json_file, args.index)

