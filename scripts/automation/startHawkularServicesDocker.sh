#!/bin/sh

HS_IMAGE="docker.io/hawkularqe/hawkular-services"
CASSANDRA_IMAGE="cassandra:3.7"

HS_START_CMD="docker run -d  -e TEST_MODE=true -e CASSANDRA_NODES=myCassandra -e DB_TIMEOUT=300 -p 8080:8080 -p 8443:8443 --link myCassandra:myCassandra ${HS_IMAGE}"
CASSANDRA_START_CMD="docker run -d --name myCassandra -e CASSANDRA_START_RPC=true ${CASSANDRA_IMAGE}"

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

exit 0

# Poll / Wait for HS to be ready
# Ex: curl http://<IP:PORT>/hawkular/metrics/status
# Output: {"MetricsService":"STARTED","Implementation-Version":"0.18.0.Final","Built-From-Git-SHA1":"d5281e70603719809bdada72249b9330b22ebf96"}
#         {"MetricsService":"FAILED","Implementation-Version":"0.18.0.Final","Built-From-Git-SHA1":"d5281e70603719809bdada72249b9330b22ebf96"}[root@vnguyen-docker2 ~]#

#end=$((SECONDS+300))

#while [ $SECONDS -lt $end ]; do
#     Do Curl
#done
