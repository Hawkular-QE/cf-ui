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

# Stop and Start CFME
dockerStopRemoveAndStart "cloudforms" "cloudforms"

#Wait while URL is loaded.
checkURL
waitForCFME "/var/www/miq/vmdb/log/evm.log"


# will fail - image has dependent child images
#dockerStopAndRm "cfme" "cfme"


