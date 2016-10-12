#!/bin/sh
source ${DIR}/../common/common.sh

export HS_IMAGE="$DOCKER_HOST_BREW/hawkular/hawkular-services:latest"
export CASSANDRA_IMAGE="$DOCKER_HOST_BREW/jboss/cassandra:latest"
export EAP7_HAWKUALR_AGENT_IMAGE="$DOCKER_HOST_BREW/jboss/jboss-eap-7-hawkular-agent:latest"
export EAP7_PULL_IMAGE="$DOCKER_HOST_BREW/jboss-eap-7-tech-preview/eap70"

export HS_PORT=8080
export HS_SECURED_PORT=9443
export HS_MGMT_PORT=9990
export HS_URL="http://`hostname`:$HS_PORT"
export HS_MAX_WAIT=600

export EAP7_PORT=9080
export EAP7_MGMT_PORT=10090
export EAP7_APP_PORT=10990
export EAP7_BOTH_OFFSET=200

export CASSANDRA_START_CMD="docker run --name hawkular-cassandra -d -e CASSANDRA_START_RPC=true ${CASSANDRA_IMAGE}"
# export HS_START_CMD="docker run -d  -e TEST_MODE=true -e CASSANDRA_NODES=HawkularServicesCassandra -e DB_TIMEOUT=300 -p 8080:${HS_PORT} -p 8443:${HS_SECURED_PORT} --link HawkularServicesCassandra:HawkularServicesCassandra ${HS_IMAGE}"
export HS_START_CMD="docker run -d --link=hawkular-cassandra -e CASSANDRA_NODES=hawkular-cassandra -e HAWKULAR_BACKEND=remote -p ${HS_PORT}:8080 -p ${HS_SECURED_PORT}:8443 -p ${HS_MGMT_PORT}:9990 ${HS_IMAGE}"

export EAP7_PULL_CMD="docker pull $EAP7_PULL_IMAGE"
export EAP7_START_STANDALONE_CMD="docker run -d --name eap7standalone -e HAWKULAR_SERVER=\"http://$(hostname):$HS_PORT\" -e JBOSS_SERVER_MODE=standalone -p $EAP7_PORT:8080 -p $EAP7_MGMT_PORT:9090 -p $EAP7_APP_PORT:9990 ${EAP7_HAWKUALR_AGENT_IMAGE}"
export EAP7_START_DOMAIN_CMD="docker run -d --name eap7domain -e HAWKULAR_SERVER=\"http://$(hostname):$HS_PORT\" -p $(($EAP7_PORT + $EAP7_BOTH_OFFSET)):8080 -p $(($EAP7_MGMT_PORT + $EAP7_BOTH_OFFSET)):9090 -p $(($EAP7_APP_PORT + $EAP7_BOTH_OFFSET)):9990 ${EAP7_HAWKUALR_AGENT_IMAGE}"

# eap7 mode <standalone|domain|both>, if not set EAP7 is not used
# export EAP7_MODE=both
