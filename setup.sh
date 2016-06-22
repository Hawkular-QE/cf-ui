#!/bin/bash

HOME=`pwd`

# Setup virtual environment
virtualenv .cf-ui
source .cf-ui/bin/activate

# Install base requirements
pip install -r requirements.txt

## Begin - Install mgmtsystem

# Needed for RHEL7
cat /etc/os-release | grep -q "Red Hat Enterprise Linux"
if [ $? -eq "0" ]
then
    echo -e "\nInstalling RHEL dependencies..."
    pip install setuptools --upgrade
fi

pip uninstall --yes pycurl
export PYCURL_SSL_LIBRARY=nss
pip install pycurl

pip install mgmtsystem

## End - Install mgmtsystem

echo -e "\nSetup Complete."
