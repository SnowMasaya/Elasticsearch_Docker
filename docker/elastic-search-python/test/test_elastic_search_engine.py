#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from os import path
APP_ROOT = path.dirname( path.abspath( __file__ ) )
from elastic_search_engine import ElasticSearchEngine
import subprocess


class Test_Elastic_Search_Engine(unittest.TestCase):
    """regist the data into the elastic Search"""

    def setUp(self):
        cmd = "cd .. && sh ./shell/elastic_search_setting.sh"
        subprocess.call( cmd, shell=True  )
        # setting elastic search
        self.elastic_search = ElasticSearchEngine()

    def test_make_doc(self):
        setting_json = APP_ROOT + "/../data/tmp.json"
        setting_index = 1
        self.elastic_search.regist_data(setting_json, setting_index)
        self.assertEqual(setting_json, self.elastic_search.json_file)

    def test_search(self):
        self.elastic_search.search_data("Ubuntu")
        test_json_data = {'body_text': '今回、作成したUbuntuでのDocker環境の構築方法です。他のディストリビューションやバージョンを試したい方は下記をご参照ください。'}
        self.assertEqual(test_json_data, self.elastic_search.search_result[0])


if __name__ == '__main__':
    unittest.main()
