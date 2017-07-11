#!/bin/bash

TOOLS=tools
OC=${TOOLS}/oc
OC_ZIP=${OC}.zip

if [ ! -f ${OC} ]; then
    unzip ${OC_ZIP} -d tools
    if [ $? -ne 0 ]; then
        echo "Error unzipping:${OC_ZIP}"
        exit 1
    fi
else
    echo "${OC} found"
fi
