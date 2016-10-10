#!/bin/bash
# ------------------------------------------------------------------
# [Masaya Ogushi] Elastic Search Regist shell
#
#    library for Unix shell scripts.
#    Usage
#           you have to use this script `sudo` command in the docker enviroment
#    Reference
#        http://dev.classmethod.jp/tool/jq-manual-japanese-translation-roughly/
#
# ------------------------------------------------------------------
if [ $# -ne 1 ]; then
    echo "$0 [Data directory]"
    exit 1
fi
# -- Body ---------------------------------------------------------
#  SCRIPT LOGIC GOES HERE
# Regist json bulk
DATA_DIR=$1
sudo chmod -R 777 ${DATA_DIR}/
ls ${DATA_DIR}/*.json.gz > ${DATA_DIR}/json_gz_list
for json_gz in `cat ${DATA_DIR}/json_gz_list`
do
    sh shell/elastic_regist_search_json_gz.sh $json_gz
done
sleep 10s
# Check the regist data
curl 'localhost:9200/_cat/indices?v'
# -----------------------------------------------------------------
