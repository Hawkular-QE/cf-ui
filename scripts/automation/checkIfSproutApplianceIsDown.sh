#!/bin/sh
# Request new appliance if MIQ host is not up - http://stackoverflow.com/a/10626193 &
# http://unix.stackexchange.com/questions/84814/health-check-of-web-page-using-curl

rm -rf ${WORKSPACE}/sprout_new.properties
touch ${WORKSPACE}/sprout_new.properties

NEW_MIQ_HOSTNAME="$(cat sprout_appliance_pool_ip.txt) "
curl "https://$NEW_MIQ_HOSTNAME" -s -f -o /dev/null || echo "Sprout appliance is DOWN.. will request new MIQ host." | \
echo "MIQ_HOSTNAME=SproutNew" > ${WORKSPACE}/sprout_new.properties
