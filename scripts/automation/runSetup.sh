#!/bin/sh

if [ "$RUN_SETUP" = true ] ; then
echo "Running ./setup.sh"
# preparing environment should not depend on browser
./setup.sh
else
echo "Not running ./setup.sh - debug mode"
fi
