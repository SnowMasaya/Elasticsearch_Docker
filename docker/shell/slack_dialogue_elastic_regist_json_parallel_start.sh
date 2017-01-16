#!/bin/bash
# ------------------------------------------------------------------
# [Masaya Ogushi] Slack and Elasticsearch Start
#
#    Usage:
#        sh shell/slack_dialogue_elastic_regist_json_parallel_start.sh [PIPE_NUMBER] [PARALLEL_NUMBER]
# ------------------------------------------------------------------
# -- Function ---------------------------------------------------------
logdate ()
{
            date "+[%Y-%m-%d %H:%M:%S] [$(basename $0)]"
}

# -- Body ---------------------------------------------------------
#  SCRIPT LOGIC GOES HERE
if [ $# -ne 2 ]; then
    echo "$0 [PIPE_NUMBER] [PARALLEL_NUMBER] "
    exit 1
fi

# ENV Viable
ELS_CONTAINER_NAME="elasticsearch_dialogue"
ELS_IMAGE_NAME="masayaresearch/elasticsearch_japanese_parallel"
DIALOGUE_IMAGE_NAME="masayaresearch/slack_dialogue"
PIPE_NUMBER=$1
PARALLEL_NUMBER=$2
VAGRANT_DATA_DIR=/home/vagrant/elastic-search-docker_parallel/python
DOCKER_DATA_DIR=/usr/share/elasticsearch/python
JSON_DATA_DIR=/usr/share/elasticsearch/python/Data/split_data

# Check the Elasticsearch Container Image
IMAGE_ID=`docker images | grep "$ELS_IMAGE_NAME" | awk '{ print $3 }' | tail -1`
if [ "$IMAGE_ID" = "" ]; then
            echo "`logdate` [info] no $ELS_IMAGE_NAME image"
            exit 1
fi
echo "`logdate` [info] IMAGE_ID=$IMAGE_ID"


# Start Elastic Search
### Check Container Name
if [ "$ELS_CONTAINER_NAME" == "" ]; then
            echo "`logdate` [error] no ELS_CONTAINER_NAME defined"
            exit 1
fi
echo "`logdate` [info] ELS_CONTAINER_NAME=$ELS_CONTAINER_NAME"

# Check Container Running
if docker ps | grep "$ELS_CONTAINER_NAME" ; then
            echo "`logdate` [info] elasticsearch is running"
            exit 0
else
    echo "`logdate` [info] docker run -d -v ${VAGRANT_DATA_DIR}:${DOCKER_DATA_DIR} --name $ELS_CONTAINER_NAME -p 9200:9200 -it ${ELS_IMAGE_NAME} /sbin/init"
    if ! docker run -d -v ${VAGRANT_DATA_DIR}:${DOCKER_DATA_DIR} --name $ELS_CONTAINER_NAME -p 9200:9200 -it ${ELS_IMAGE_NAME} /sbin/init; then
            echo "`logdate` [error] failed to run elasticsearch"
                 exit 1
    fi
fi

# Setting the Elasticsearch Enviroments
echo "`logdate` [info] docker exec -it $ELS_CONTAINER_NAME sh shell/elastic_search_setting.sh"
if ! docker exec -it $ELS_CONTAINER_NAME sh shell/elastic_search_setting.sh; then
            echo "`logdate` [error] failed to start elasticsearch"
            exit 1
fi

# Regist Data for the Elasticsearch
echo "`logdate` [info] docker exec -it $ELS_CONTAINER_NAME sh shell/elastic_regist_search_json_parallel.sh $PIPE_NUMBER $PARALLEL_NUMBER ${JSON_DATA_DIR}"
if ! docker exec -it $ELS_CONTAINER_NAME sh shell/elastic_regist_search_json_parallel.sh $PIPE_NUMBER $PARALLEL_NUMBER ${JSON_DATA_DIR} ; then
            echo "`logdate` [error] failed to regist elasticsearch"
            exit 1
fi

# Check the Dialogue Container Image
DIALOGUE_IMAGE_ID=`docker images | grep "$DIALOGUE_IMAGE_NAME" | awk '{ print $3 }' | tail -1`
if [ "$IMAGE_ID" = "" ]; then
            echo "`logdate` [info] no $DIALOGUE_IMAGE_NAME image"
            exit 1
fi
echo "`logdate` [info] IMAGE_ID=$DIALOGUE_IMAGE_ID"

# Start Dialogue
echo "`logdate` [info] docker run --link $ELS_CONTAINER_NAME -it $DIALOGUE_IMAGE_ID bash"
if ! docker run --link $ELS_CONTAINER_NAME -it $DIALOGUE_IMAGE_ID bash; then
            echo "`logdate` [error] failed to start dialogue"
            exit 1
fi
# -----------------------------------------------------------------