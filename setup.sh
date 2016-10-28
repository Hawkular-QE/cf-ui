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

pip install mgmtsystem==1.4.10

# setup test recorder
pip install http://pypi.python.org/packages/source/v/vnc2flv/vnc2flv-20100207.tar.gz
mkdir records

# setup flv2gif converter
pip install moviepy

## End - Install mgmtsystem

echo -e "\nSetup Complete."
