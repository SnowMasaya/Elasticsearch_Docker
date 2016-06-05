#!/bin/bash
# ------------------------------------------------------------------
# [Masaya Ogushi] Elastic First Setting
#
#          library for Unix shell scripts.
#          Reference
#              https://medium.com/hello-elasticsearch/elasticsearch-6d69b6ff5c26#.94u8w1vgp
#
# ------------------------------------------------------------------

# -- Body ---------------------------------------------------------
#  SCRIPT LOGIC GOES HERE
ROOT_DIR=`pwd`

# Setting Elastic Search
sudo /etc/init.d/elasticsearch start &
sleep 10s
curl -XPUT localhost:9200/_template/contents --data-binary "@config/elastic_index_template.json"
sudo /etc/init.d/elasticsearch stop &
sleep 2s
elasticsearch -Des.security.manager.enabled=false &
sleep 8s
# Register command
echo Register
curl -X POST http://localhost:9200/contents-20160111/contents/1  -d '
{
    "body_text" : "今回、作成したUbuntuでのDocker環境の構築方法です。他のディストリビューションやバージョンを試したい方は下記をご参照ください。"
}
'
# Search Command
sleep 1s
echo Search
curl -XGET 'localhost:9200/contents-20160111/contents/_search?pretty' -d'
{
 "query":{"match":{"body_text":"Ubuntu"}}
}'
# -----------------------------------------------------------------
