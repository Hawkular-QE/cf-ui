#!/bin/sh

export DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# choose env via scripts first arg or CF_UI_HS_ENV_SOURCE env variable, for both options string needs to be set to path to `source`
if [ ! -z "$1" ]  ; then
  echo "Using env variables in $1"
  source ${DIR}/$1
elif [[ $CF_UI_CFME_ENV_SOURCE && ${CF_UI_CFME_ENV_SOURCE-x} ]] ; then
  echo "Using $CF_UI_CFME_ENV_SOURCE.sh to export env variables"
  source ${DIR}/$CF_UI_CFME_ENV_SOURCE
else
  echo "Using default env variables"
  source ${DIR}/setDefaultEnv.sh
fi

changeRegister

dockerStopAndRm "cloudforms/cfme-middleware" "cloudforms/cfme-middleware"

# will fail - image has dependent child images
dockerStopAndRm "cfme" "cfme"

# Start CFME

echo "Creating ${CFME_IMAGE}"
${CFME_CREATE_CMD}
# change necessary
docker cp cloudforms-temp:/var/www/miq/vmdb/config/permissions.yml .
echo "- :mdl" >> permissions.yml
# echo "- :ems-type:hawkular" >> permissions.yml
echo "- ems-type:hawkular" >> permissions.yml
docker cp permissions.yml cloudforms-temp:/var/www/miq/vmdb/config/permissions.yml
docker commit cloudforms-temp cloudforms/cfme-middleware
echo "Starting ${CFME_IMAGE}"
${CFME_START_CMD}

waitForCFME "/var/www/miq/vmdb/log/evm.log"
