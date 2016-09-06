#!/bin/sh

# choose env via scripts first arg or CF_UI_HS_ENV_SOURCE env variable, for both options string needs to be set to path to `source`
if [[ $1 && ${1-x} ]] ; then
  echo "Using env variables in $1"
  source $1
elif [[ $CF_UI_HS_ENV_SOURCE && ${CF_UI_HS_ENV_SOURCE-x} ]] ; then
  echo "Using $CF_UI_HS_ENV_SOURCE.sh to export env variables"
  source "$(pwd)"/$CF_UI_HS_ENV_SOURCE
else
  echo "Using default env variables"
  source "$(pwd)"/setDefaultEnv.sh
fi

HS_START_CMD="docker run -d  -e TEST_MODE=true -e CASSANDRA_NODES=HawkularServicesCassandra -e DB_TIMEOUT=300 -p 8080:${HS_PORT} -p 8443:${HS_SECURED_PORT} --link HawkularServicesCassandra:HawkularServicesCassandra ${HS_IMAGE}"
CASSANDRA_START_CMD="docker run -d --name HawkularServicesCassandra -e CASSANDRA_START_RPC=true ${CASSANDRA_IMAGE}"

# Stop HS if running
HS_CONTAINER_ID=`docker ps | grep $HS_IMAGE | awk '{ print $1}'`

if [ ${#HS_CONTAINER_ID} -gt 0 ] ; then
    echo "Stopping HS Container ${HS_CONTAINER_ID}"
    docker stop ${HS_CONTAINER_ID}
    docker rm ${HS_CONTAINER_ID}
    IMAGE_ID=`docker images | grep "hawkular-services" | awk '{ print $3}'`
    echo "Removing Image ${HS_IMAGE}   ID: ${IMAGE_ID}"
    docker rmi -f ${IMAGE_ID}
else
    echo "No ${HS_IMAGE} container found to be running."
fi

# Stop Cassandra if running
CASSANDRA_CONTAINER_ID=`docker ps | grep ${CASSANDRA_IMAGE} | awk '{print $1}'`

echo "SIZE: $CASSANDRA_CONTAINER_ID"
if [ ${#CASSANDRA_CONTAINER_ID} -gt 0 ] ; then
    echo "Stopping HS Container ${CASSANDRA_CONTAINER_ID}"
    docker stop ${CASSANDRA_CONTAINER_ID}
    docker rm ${CASSANDRA_CONTAINER_ID}
    IMAGE_ID=`docker images | grep "cassandra" | awk '{print $3}'`
    echo "Removing Image ${CASSANDRA_IMAGE}   ID: ${IMAGE_ID}"
    docker rmi -f ${IMAGE_ID}
else
    echo "No ${CASSANDRA_IMAGE} container found to be running."
fi


# Start Cassandra
echo "Starting ${CASSANDRA_IMAGE}"
${CASSANDRA_START_CMD}

sleep 5

# Start HS
echo "Starting ${HS_IMAGE}"
${HS_START_CMD}

# wait for HS to be up
time=0
while [ $time -lt $HS_MAX_WAIT ];
do
    echo "Trying to get ${HS_URL}/hawkular/inventory/status"
    responseInventory=`curl -s -H "Content-Type: application/json" "${HS_URL}/hawkular/inventory/status"`
    echo "Got response ${responseInventory}"
    echo "Trying to get ${HS_URL}/hawkular/metrics/status"
    responseMetrics=`curl -s -H "Content-Type: application/json" "${HS_URL}/hawkular/metrics/status"`
    echo "Got response ${responseMetrics}"
    if [[ $responseInventory == *"true"* && $responseMetrics == *"STARTED"* ]]
    then
        echo "Hawkular was started succesfully in ${time}s"
        exit 0
        return
    fi
    echo "Waiting for Hawkular server to start... ${time}s"
    sleep 10s
    let time+=10
done
echo "Hawkular failed or timed out to startup!!"
exit 1
