#!/bin/sh

source ${DIR}/../common/common.sh

export CFME_IMAGE="$DOCKER_HOST_BREW/cloudforms/cfme58:latest"

export CFME_PORT=80
export CFME_SECURED_PORT=443
export POSTGRESQL_PORT=5432

export CFME_START_CMD="docker run --privileged -di -p $CFME_PORT:80 -p $CFME_SECURED_PORT:443 -p $POSTGRESQL_PORT:5432 $DOCKER_HOST_BREW/cloudforms/cfme58:latest"
