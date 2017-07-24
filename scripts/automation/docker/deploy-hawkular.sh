#!/bin/bash

OS_SERVER_=
OS_USERNAME_=
OS_PASSWORD_=
OS_PROJECT_=

HAWKULAR_APP_="https://raw.githubusercontent.com/hawkular/hawkular-services/master/openshift/hawkular-services-ephemeral.yaml"
HAWKULAR_IMAGE_='hawkular/hawkular-services:latest'
HAWKULAR_USERNAME_="jdoe"
HAWKULAR_PASSWORD_="password"

OC_="/usr/bin/oc"

# Note: May want to set these vars via Jenkins job parameters

if [[ -n $HAWKULAR_APP ]]; then
    HAWKULAR_APP_=${HAWKULAR_APP}
elif [ -z $HAWKULAR_APP_ ]; then
    echo "Error: HAWKULAR_API_ not set"
    exit 1
fi

if [[ -n $OS_SERVER ]]; then
    OS_SERVER_=${OS_SERVER}
elif [ -z $OS_SERVER_ ]; then
    echo "Error: OS_SERVER_ not set"
    exit 1
fi

if [[ -n $OS_USERNAME ]]; then
    OS_USERNAME_=${OS_USERNAME}
elif [ -z $OS_USERNAME_ ]; then
    echo "Error: OS_USERNAME_ not set"
    exit 1
fi

if [[ -n $OS_PASSWORD ]]; then
    OS_PASSWORD_=${OS_PASSWORD}
elif [ -z $OS_PASSWORD_ ]; then
    echo "Error: PASSWORD_ not set"
    exit 1
fi

if [[ -n $OS_PROJECT ]]; then
    OS_PROJECT_=${OS_PROJECT}
elif [ -z $OS_PROJECT_ ]; then
    echo "Error: PROJECT_ not set"
    exit 1
fi

if [[ -n $HAWKULAR_IMAGE ]]; then
    HAWKULAR_IMAGE_=${HAWKULAR_IMAGE}
elif [ -z $HAWKULAR_IMAGE_ ]; then
    echo "Error: HAWKULAR_IMAGE_ not set"
    exit 1
fi

if [[ -n $HAWKULAR_USERNAME ]]; then
    HAWKULAR_USERNAME_=${HAWKULAR_USERNAME}
elif [ -z $HAWKULAR_USERNAME_ ]; then
    echo "Error: HAWKULAR_USERNAME_ not set"
    exit 1
fi

if [[ -n $HAWKULAR_PASSWORD ]]; then
    HAWKULAR_PASSWORD_=${HAWKULAR_PASSWORD}
elif [ -z $HAWKULAR_PASSWORD_ ]; then
    echo "Error: PASSWORD_ not set"
    exit 1
fi

if [[ -n $OC ]]; then
    OC_=${OC}
elif [ -z $OC_ ]; then
    echo "Error: OC_ not set"
    exit 1
fi

echo "OC: ${OC_}"
echo "OS_SERVER: ${OS_SERVER_}, OS_USERNAME: ${OS_USERNAME_}, OS_PASSWORD: ${OS_PASSWORD_}, OS_PROJECT: ${OS_PROJECT_}"
echo "HAWKULAR_APP: ${HAWKULAR_APP_}"
echo "HAWKULAR_IMAGE: ${HAWKULAR_IMAGE_}, HAWKULAR_USERNAME: ${HAWKULAR_USERNAME_}, HAWKULAR_PASSWORD: ${HAWKULAR_PASSWORD_}"

${OC_} login ${OS_SERVER_} -u=${OS_USERNAME_} -p=${OS_PASSWORD_} --insecure-skip-tls-verify
if [ $? -ne 0 ]; then
    echo "Failed to login Server:${OS_SERVER_} Username:${OS_USERNAME_} Password:${OS_PASSWORD_}"
    exit 1
fi

${OC_} get projects | grep ${OS_PROJECT_}
if [ $? -eq 0 ]; then
    echo "Deleting project:${OS_PROJECT_}"
    ${OC_} delete project ${OS_PROJECT_}
    if [ $? -ne 0 ]; then
        echo "Failed to delete project: ${OS_PROJECT_}"
        exit 1
    fi

    while true; do
        ${OC_} get projects | grep ${OS_PROJECT_}
        if [ $? -ne 0 ]; then
            break
        fi
        sleep 2
    done
fi

echo "Creating project:${OS_PROJECT_}"
${OC_} new-project ${OS_PROJECT_} --description="Hawkular Services" --display-name=${OS_PROJECT_}
if [ $? -ne 0 ]; then
    echo "Failed to create project:${OS_PROJECT_}"
    exit 1
fi

echo "Deploy App"
${OC_} process -f ${HAWKULAR_APP_} -v "HAWKULAR_SERVICES_IMAGE=${HAWKULAR_IMAGE_},HAWKULAR_USER=${HAWKULAR_USERNAME_},HAWKULAR_PASSWORD=${HAWKULAR_PASSWORD_}" |  ${OC_} create -f -
if [ $? -ne 0 ]; then
    echo "Failed to deploy app: ${OS_PROJECT_}"
    exit 1
fi

echo "App deployed"

ROUTE=`${OC_} get routes | grep ${OS_PROJECT_} | awk '{print $2}'`
URL="http://${ROUTE}"
echo "App URL: ${URL}"


