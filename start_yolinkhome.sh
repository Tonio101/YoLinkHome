#!/bin/bash

FLOCK=/usr/bin/flock
LOCK_FILE=/tmp/yolinkhome.lockfile
FLOCK_OPTS="-n"

YOLINK_PATH=$HOME/YoLinkHome/src
YOLINK_FILE=yolink.py
YOLINK_DFILE=yolink_data.yml

YOLINK_SCRIPT=$YOLINK_PATH/$YOLINK_FILE
DATA_FILE=$YOLINK_PATH/$YOLINK_DFILE

HTTP_API=${SVR_URL}/openApi
# Remove HTTPS:// prefix
MQTT_URL=${SVR_URL}
MQTT_PORT=8003
CSID=${CSID}
CSSECKEY=${CSSECKEY}
TOPIC=${CSName}/report

YOLINK_ARGS="--url $HTTP_API
             --mqtt_url $MQTT_URL 
             --mqtt_port $MQTT_PORT
             --csid $CSID
             --csseckey $CSSECKEY
             --topic $TOPIC
             --file $DATA_FILE"

$FLOCK $FLOCK_OPTS $LOCK_FILE $YOLINK_SCRIPT $YOLINK_ARGS
