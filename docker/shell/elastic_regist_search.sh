#!/bin/bash
# ------------------------------------------------------------------
# [Masaya Ogushi] Elastic Search Regist shell
#
#          library for Unix shell scripts.
#          Usage
#             you have to use this script `sudo` command in the docker enviroment
#          Reference
#              http://dev.classmethod.jp/tool/jq-manual-japanese-translation-roughly/
#
# ------------------------------------------------------------------

# -- Body ---------------------------------------------------------
#  SCRIPT LOGIC GOES HERE
ROOT_DIR=`pwd`
LIST_DIR=$ROOT_DIR/data

# split json file
for split_json in $(ls $LIST_DIR/*.json)
do
  url_count=`jq ".[].body_text" $split_json | wc | awk '{print $1;}'`
  echo $url_count
  url_counter=$(($url_count - 1 ))
  echo $url_counter
  for count in $(seq 1 $url_counter)
    do
    sudo touch ${split_json}_tmp.json
    sudo chmod 777 ${split_json}_tmp.json
    jq ".[$count]" $split_json > ${split_json}_tmp.json
    /usr/local/venv/3.5.0/bin/python $ROOT_DIR/elastic-search-python/execute/execute_elastic_search.py -j ${split_json}_tmp.json -i $count
  done
done
# Check the regist data
curl 'localhost:9200/_cat/indices?v'
# -----------------------------------------------------------------