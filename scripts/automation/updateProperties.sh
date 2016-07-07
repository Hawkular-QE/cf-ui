#!/bin/sh
# repalce parameters for current build
sed -i "/HAWKULAR_HOSTNAME /c\HAWKULAR_HOSTNAME = $HAWKULAR_HOSTNAME" conf/properties.properties
sed -i "/MIQ_HOSTNAME /c\MIQ_HOSTNAME = $MIQ_HOSTNAME" conf/properties.properties
sed -i "/HAWKULAR_PORT /c\HAWKULAR_PORT = $HAWKULAR_PORT" conf/properties.properties
sed -i "/DISPLAY_PORT /c\DISPLAY_PORT = $DISPLAY_PORT" conf/properties.properties
sed -i "/RECORD_TESTS /c\RECORD_TESTS = True" conf/properties.properties
