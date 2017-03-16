#!/bin/sh

# common functions for docker wrappers
# make sure all necessary env variables are imported
export PORT_INSECURE_REGISTRY=8888

export DOCKER_HOST_BREW="brew-pulp-docker01.web.prod.ext.phx2.redhat.com:$PORT_INSECURE_REGISTRY"

export TECH_PREVIEW_IMAGE="$DOCKER_HOST_BREW/jboss-eap-7-tech-preview/eap70"
export INSECURE_REGISTER_STRING="INSECURE_REGISTRY='--insecure-registry $DOCKER_HOST_BREW'"
export TECH_PREVIEW_PULL_CMD="docker pull $TECH_PREVIEW_IMAGE"


# reusing jon utils install_eap7-standalone.sh
function waitForCFME {
local time=0
# takes some time
echo "sleep 30s"
sleep 30s
local CFME_CONTAINER_ID=`docker ps | grep "cloudforms" | awk '{print $1}'`
echo "CFME_CONTAINER_ID: $CFME_CONTAINER_ID"
local log=$1
echo "log: $log"
sleep 5s
while [ $time -lt 180 ];
do
  finished=$(docker exec -i $CFME_CONTAINER_ID grep -c '.*MiqServer id: 1.* status: "started".*has_active_userinterface: true.*has_active_webservices: true' $log | grep -v errors)
  if [ "$finished" != "0" ];
  then
    echo "CFME was started succesfully"
    # to be sure
    sleep 5s
    return 0
  fi
  echo "Waiting for CFME to start..."
  sleep 3s
  let time+=3
done
}

function waitForHS(){
  # wait for HS to be up
  time=0
  while [ $time -lt $HS_MAX_WAIT ];
  do
      echo "Trying to get ${HS_URL}/hawkular/inventory/status"
      local responseInventory=`curl -s -H "Content-Type: application/json" "${HS_URL}/hawkular/inventory/status"`
      echo "Got response ${responseInventory}"
      echo "Trying to get ${HS_URL}/hawkular/metrics/status"
      local responseMetrics=`curl -s -H "Content-Type: application/json" "${HS_URL}/hawkular/metrics/status"`
      echo "Got response ${responseMetrics}"
      if [[ $responseInventory == *"true"* && $responseMetrics == *"STARTED"* ]]
      then
          echo "Hawkular was started succesfully in ${time}s"
          return 0
      fi
      echo "Waiting for Hawkular server to start... ${time}s"
      sleep 10s
      let time+=10
  done
  echo "Hawkular failed or timed out to startup!!"
  return 1
}

# reusing jon utils install_eap7-standalone.sh
function waitForEapServer {
local time=0
if [ -z "$2" ]  ; then
EAP7_CONTAINER_ID=`docker ps | grep ${EAP7_HAWKUALR_AGENT_IMAGE} | awk '{print $1}'`
else
EAP7_CONTAINER_ID=`docker ps | grep ${2} | awk '{print $1}'`
fi
echo "EAP7_CONTAINER_ID: $EAP7_CONTAINER_ID"
local log=$1
echo "log: $log"
sleep 5s
while [ $time -lt 60 ];
do
  finished=$(docker exec -i $EAP7_CONTAINER_ID grep -c "JBoss EAP.*started." $log | grep -v errors)
  if [ "$finished" == "1" ];
  then
    echo "EAP7 Stadnalone Server was started succesfully"
    return 0
  fi
  echo "Waiting for standalone server to start..."
  sleep 3s
  let time+=3
done
}

function dockerStopAndRm(){
  # Stop image if running
  local image=$1
  local imageName=$2
  CONTAINER_ID=`docker ps -a | grep ${image} | awk '{print $1}'`

  echo "dockerStopAndRm: Container id: $CONTAINER_ID"
  if [ ${#CONTAINER_ID} -gt 0 ] ; then
      echo "Stopping Container ${CONTAINER_ID}"
      docker stop ${CONTAINER_ID}
      docker rm ${CONTAINER_ID}
      IMAGE_ID=`docker images | grep "$imageName" | awk '{print $3}'`
      echo "Removing Image ${image}   ID: ${IMAGE_ID}"
      docker rmi -f ${IMAGE_ID}
  else
      echo "No ${image} container found to be running."
  fi
}

function dockerStopAndStart(){
 # Stop image if running and then start it again
  local image=$1
  CONTAINER_ID=`docker ps -a | grep ${image} | awk '{print $1}'`

  echo "dockerStopAndstart: Container id: $CONTAINER_ID"
  if [ ${#CONTAINER_ID} -gt 0 ] ; then
      echo "Stopping Container ${CONTAINER_ID}"
      docker stop ${CONTAINER_ID}
      docker start ${CONTAINER_ID}
  else
      echo "No ${image} container found to be running."
      echo "Creating and starting CFME container."
      ${CFME_START_CMD}
  fi
}


function checkURL(){
# Check if URL exist else wait while it loads
    local URL=https://10.8.187.112
    while ! ($(curl -k "$URL" | grep 'title="Login"'));
    do
        echo "Waiting to load the '$URL'"
        sleep 5
    done


function stopEAP(){
  # Stop EAP7 if running
  local EAP7_IMAGE=$1
  local eap7mode=$2
  local EAP7_HAWKUALR_AGENT_IMAGE_MODED="$EAP7_IMAGE.*$eap7mode"

  dockerStopAndRm "$EAP7_HAWKUALR_AGENT_IMAGE_MODED" "jboss-eap-7-hawkular-agent.*"
}

# change register
function changeRegister(){
  # correct registry name, including the port number (8888)
  echo "INSECURE_REGISTER_STRING: $INSECURE_REGISTER_STRING"
  if [ -f /etc/sysconfig/docker ] ; then
    if ! grep -q "$DOCKER_HOST_BREW" /etc/sysconfig/docker ; then
      echo "Adding ${INSECURE_REGISTER_STRING} to /etc/sysconfig/docker and restarting docker daemon"
      echo "${INSECURE_REGISTER_STRING}" >> /etc/sysconfig/docker
      systemctl restart docker
    fi
  else
    # TODO test this
    if ! grep -q "$DOCKER_HOST_BREW" /etc/docker/daemon.json ; then
      echo "Adding ${INSECURE_REGISTER_STRING} to /etc/docker/daemon.json and restarting docker daemon"
      touch /etc/docker/daemon.json
      echo '{ "insecure-registries":["brew-pulp-docker01.web.prod.ext.phx2.redhat.com:8888"] }' >> /etc/docker/daemon.json
      service docker restart
    fi
  fi
}
