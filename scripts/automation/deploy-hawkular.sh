#!/bin/bash

HAWKULAR_APP="https://raw.githubusercontent.com/hawkular/hawkular-services/master/openshift/hawkular-services-ephemeral.yaml"

OS_SERVER=
OS_USERNAME=
OS_PASSWORD=
OS_PROJECT=

HAWKULAR_IMAGE='hawkular/hawkular-services:latest'
USERNAME="jdoe"
PASSWORD="password"

OC="./oc"

# Override Openshift Server and CREDs if set externally
# Note: May want to set these vars via Jenkins job parameters
if [ -n "${EXTERN_OS_SERVER}" ]; then
    echo "Setting OS_SERVER: ${EXTERN_OS_SERVER}"
    OS_SERVER=${EXTERN_OS_SERVER}
fi

if [ -n "${EXTERN_OS_USERNAME}" ]; then
    echo "Setting OS_USERNAME: ${EXTERN_OS_USERNAME}"
    OS_USERNAME=${EXTERN_OS_USERNAME}
fi

if [ -n "${EXTERN_OS_PASSWORD}" ]; then
    echo "Setting OS_PASSWORD: ${EXTERN_OS_PASSWORD}"
    OS_PASSWORD=${EXTERN_OS_PASSWORD}
fi

if [ -n "${EXTERN_OS_PROJECT}" ]; then
    echo "Setting OS_PROJECT: ${EXTERN_OS_PROJECT}"
    OS_PROJECT=${EXTERN_OS_PROJECT}
fi
echo "OS_SERVER: ${OS_SERVER}"
echo "OS_USERNAME: ${OS_USERNAME}"
echo "OS_PASSWORD: ${OS_PASSWORD}"
echo "OS_PROJECT: ${OS_PROJECT}"

${OC} login ${OS_SERVER} -u=${OS_USERNAME} -p=${OS_PASSWORD} --insecure-skip-tls-verify
if [ $? -ne 0 ]; then
    echo "Failed to login Server:${OS_SERVER} Username:${USERNAME} Password:${PASSWORD}"
    exit 1
fi

${OC} get projects | grep ${OS_PROJECT}
if [ $? -eq 0 ]; then
    echo "Deleting project:${OS_PROJECT}"
    ${OC} delete project ${OS_PROJECT}
    if [ $? -ne 0 ]; then
        echo "Failed to delete project: ${OS_PROJECT}"
        exit 1
    fi

    while true; do
        ${OC} get projects | grep ${OS_PROJECT}
        if [ $? -ne 0 ]; then
            break
        fi
        sleep 2
    done
fi

echo "Creating project:${OS_PROJECT}"
${OC} new-project ${OS_PROJECT} --description="Hawkular Services" --display-name=${OS_PROJECT}
if [ $? -ne 0 ]; then
    echo "Failed to create project:${OS_PROJECT}"
    exit 1
fi

echo "Deploy App"
${OC} process -f ${HAWKULAR_APP} -v "HAWKULAR_SERVICES_IMAGE=${HAWKULAR_IMAGE},HAWKULAR_USER=${USERNAME},HAWKULAR_PASSWORD=${PASSWORD}" |  ${OC} create -f -
if [ $? -ne 0 ]; then
    echo "Failed to delete project: ${OS_PROJECT}"
    exit 1
fi

echo "App deployed"

ROUTE=`${OC} get routes | grep ${OS_PROJECT} | awk '{print $2}'`
URL="http://${ROUTE}"
echo "App URL: ${URL}"

