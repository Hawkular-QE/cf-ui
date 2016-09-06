#!/bin/sh

export HS_IMAGE="docker.io/HSqe/HS-services"
export CASSANDRA_IMAGE="cassandra:3.7"
export HS_PORT=8080
export HS_SECURED_PORT=8443
export HS_URL="http://`hostname`:$HS_PORT"
export HS_MAX_WAIT=600
