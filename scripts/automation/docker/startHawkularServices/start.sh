#!/bin/sh

export DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# choose env via scripts first arg or CF_UI_HS_ENV_SOURCE env variable, for both options string needs to be set to path to `source`
if [ ! -z "$1" ]  ; then
  echo "Using env variables in $1"
  source ${DIR}/$1
elif [[ $CF_UI_HS_ENV_SOURCE && ${CF_UI_HS_ENV_SOURCE-x} ]] ; then
  echo "Using $CF_UI_HS_ENV_SOURCE.sh to export env variables"
  source ${DIR}/$CF_UI_HS_ENV_SOURCE
else
  echo "Using default env variables"
  source ${DIR}/setDefaultEnv.sh
fi

echo "EAP7_MODE: $EAP7_MODE"

changeRegister

stopEAP $EAP7_HAWKUALR_AGENT_IMAGE "domain"
stopEAP $EAP7_HAWKUALR_AGENT_IMAGE "standalone"

dockerStopAndRm "$HS_IMAGE" "hawkular-services"

dockerStopAndRm "$CASSANDRA_IMAGE" "cassandra"

# pull jboss-eap-7-tech-preview/eap70
echo "Pull ${TECH_PREVIEW_PULL_CMD}"
${TECH_PREVIEW_PULL_CMD}

# Start Cassandra
echo "Starting ${CASSANDRA_IMAGE}"
${CASSANDRA_START_CMD}

sleep 5

# Start HS
echo "Starting ${HS_IMAGE}"
${HS_START_CMD}

waitForHS

if ! [ -z "$EAP7_MODE+x" ]  ; then
  sleep 5

  # Start EAP7
  EAP7_IMAGE=$EAP7_HAWKUALR_AGENT_IMAGE
  EAP7_START_CMD=$EAP7_START_STANDALONE_CMD

  if [ "$EAP7_MODE" == "domain" ]; then
    EAP7_START_CMD=$EAP7_START_DOMAIN_CMD
  elif [ "$EAP7_MODE" == "both" ]; then
    EAP7_MODE="standalone"
    echo "Starting EAP7 in both standalone and domain modes"
    echo "Starting ${EAP7_IMAGE} in $EAP7_MODE mode"
    ${EAP7_START_CMD}

    sleep 5

    waitForEapServer "/opt/eap/$EAP7_MODE/log/server.log" "eap7$EAP7_MODE"

    EAP7_MODE="domain"
    EAP7_START_CMD=$EAP7_START_DOMAIN_CMD
  fi

  echo "Starting ${EAP7_IMAGE} in $EAP7_MODE mode"
  ${EAP7_START_CMD}

  sleep 5

  serverLogFileName="server.log"
  if [ "$EAP7_MODE" == "domain" ]; then
      serverLogFileName="host-controller.log"
  fi

  waitForEapServer "/opt/eap/$EAP7_MODE/log/$serverLogFileName" "eap7$EAP7_MODE"
fi
