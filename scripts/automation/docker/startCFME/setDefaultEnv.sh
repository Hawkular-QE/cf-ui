#!/bin/sh

source ${DIR}/../common/common.sh

export CFME_IMAGE="$DOCKER_HOST_BREW/cloudforms/cfme:cfme-5.7-rhel-7-docker-candidate-20160908134933"

export CFME_PORT=80
export CFME_SECURED_PORT=443

export CFME_CREATE_CMD="docker create --name cloudforms-temp $CFME_IMAGE"
export CFME_START_CMD="docker run --privileged -di -p $CFME_PORT:80 -p $CFME_SECURED_PORT:443 cloudforms/cfme-middleware"
