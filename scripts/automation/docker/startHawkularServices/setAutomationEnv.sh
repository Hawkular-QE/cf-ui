#!/bin/sh

export HS_IMAGE="docker.io/hawkularqe/hawkular-services"
export CASSANDRA_IMAGE="cassandra:3.7"
echo "HAWKULAR_PORT: $HAWKULAR_PORT"
export HS_PORT=$HAWKULAR_PORT
export HS_SECURED_PORT=8443
export HS_URL="http://`hostname`:$HS_PORT"
export HS_MAX_WAIT=600
