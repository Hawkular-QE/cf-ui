#!/bin/sh
# provide MIQ host as Sprout appliance

echo "Sprout old appliance pool id:"
echo "$(cat sprout_appliance_pool_id.txt)"


if [[ -f sprout_appliance_pool_id.txt ]] ; then
SPROUT_APPLIANCE_POOL_ID=`cat sprout_appliance_pool_id.txt`

echo "Destroying appliance pool with ID: $SPROUT_APPLIANCE_POOL_ID"

rm -rf sprout_destroy_pool_result.json
# stop appliance if exists by pool id in file sprout_appliance_pool_id.txt...
curl -H "Content-Type: application/json" -X POST -d '{"method":"destroy_pool","args":["'${SPROUT_APPLIANCE_POOL_ID}\
'"],"kwargs":{},"auth":["'${SPROUT_USER}'","'${SPROUT_PASSWORD}'"]}' http://10.16.4.94/appliances/api > sprout_destroy_pool_result.json

echo "Sprout destroy pool result:"
echo "$(cat sprout_destroy_pool_result.json)"

DELETE_POOL_STATUS=$(cat sprout_destroy_pool_result.json | python -c 'import json,sys;obj=json.load(sys.stdin);print(obj["status"]);')

if [[ $DELETE_POOL_STATUS != "success" ]] ; then
echo "Exception occured when trying to delete pool, it may be because pool is already destroyed, fix this manually at \
<a href='http://10.16.4.94/appliances/my'>Sprout</a> if needed"
fi

# wait until pool is destroyded
WAIT_FOR_APPLIANCE_STATUS="True"

while [[ $WAIT_FOR_APPLIANCE_STATUS = "True" ]] ; do
sleep 10s
rm -rf sprout_appliance_pool_status.json
touch sprout_appliance_pool_status.json

curl -s -H "Content-Type: application/json" -X POST -d \
'{"method":"request_check","args":["'${SPROUT_APPLIANCE_POOL_ID}'"],"kwargs":{},"auth":["'${SPROUT_USER}'","'${SPROUT_PASSWORD}'"]}' \
http://10.16.4.94/appliances/api > sprout_appliance_pool_status.json
REQUEST_APPLIANCES_RESULT=$(cat sprout_appliance_pool_status.json | python -c 'import json,sys;obj=json.load(sys.stdin);print(obj["result"]["class"]);')
echo "Waiting for pool to destroy.."
echo "$REQUEST_APPLIANCES_RESULT"
if [[ $REQUEST_APPLIANCES_RESULT = "DoesNotExist" ]]  || [[ $REQUEST_APPLIANCES_RESULT = "Exception" ]]; then
WAIT_FOR_APPLIANCE_STATUS="False"
fi
done


fi
# delete info about previous appliance
rm -rf request_appliances_result.json
touch request_appliances_result.json

# get appliace -> check and parse POOl_ID
curl -H "Content-Type: application/json" -X POST -d \
'{"method":"request_appliances","args":["upstream"],"kwargs":{"lease_time":"1440"},"auth":["'${SPROUT_USER}'","'${SPROUT_PASSWORD}'"]}' \
http://10.16.4.94/appliances/api > request_appliances_result.json

echo "Requesting appliance, result:"
echo "$(cat request_appliances_result.json)"

#
# parse result into variable
REQUEST_APPLIANCES_POOL_ID=$(cat request_appliances_result.json | python -c 'import json,sys;obj=json.load(sys.stdin);print(obj["result"]);')
#
REQUEST_APPLIANCES_STATUS=$(cat request_appliances_result.json | python -c 'import json,sys;obj=json.load(sys.stdin);print(obj["status"]);')
if [[ $REQUEST_APPLIANCES_STATUS != "success" ]]; then # TODO because this is not enough for stable solution?
echo "Failing because Sprout did not provide appliance"
exit 1
fi
rm -rf sprout_appliance_pool_id.txt

echo "$REQUEST_APPLIANCES_POOL_ID" > sprout_appliance_pool_id.txt
sleep 5s

WAIT_FOR_APPLIANCE_STATUS="True"

# 30min / 10s
MAX_WAITING_CYCLES=180


while [[ $WAIT_FOR_APPLIANCE_STATUS = "True" ]] ; do
sleep 10s
rm -rf sprout_appliance_pool_status.json
touch sprout_appliance_pool_status.json

curl -s -H "Content-Type: application/json" -X POST -d \
'{"method":"request_check","args":["'${REQUEST_APPLIANCES_POOL_ID}'"],"kwargs":{},"auth":["'${SPROUT_USER}'","'${SPROUT_PASSWORD}'"]}' \
http://10.16.4.94/appliances/api > sprout_appliance_pool_status.json
REQUEST_APPLIANCES_RESULT=$(cat sprout_appliance_pool_status.json | python -c 'import json,sys;obj=json.load(sys.stdin);print(obj["result"]);')
REQUEST_APPLIANCES_FINISHED=$(cat sprout_appliance_pool_status.json | python -c 'import json,sys;obj=json.load(sys.stdin);print(obj["result"]["finished"]);')

echo "Waiting for pool to load.. Finished: $REQUEST_APPLIANCES_FINISHED"
echo "$REQUEST_APPLIANCES_RESULT"
if [[ $REQUEST_APPLIANCES_FINISHED == "True" ]] ; then
WAIT_FOR_APPLIANCE_STATUS="False"
fi

MAX_WAITING_CYCLES=$((MAX_WAITING_CYCLES-1))
if [ $MAX_WAITING_CYCLES -eq 0 ]; then
   echo "Unable to get Sprout appliance.. exiting with 1.";
   exit 1
fi

done

# delete file with old MIQ IP
rm -rf sprout_appliance_pool_ip.txt

echo "Saving new Sprout appliance IP to file sprout_appliance_pool_ip.txt"
echo "$(cat sprout_appliance_pool_status.json | python -c \
'import json,sys;obj=json.load(sys.stdin);print(obj["result"]["appliances"][0]["ip_address"]);') " | xargs > sprout_appliance_pool_ip.txt
NEW_MIQ_IP=$(cat sprout_appliance_pool_ip.txt)

# check if IP is valid
if ! [[ $NEW_MIQ_IP =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
echo "New MIQ IP cannot be in this format.."
echo "$NEW_MIQ_IP"
# TODO rebuild job with all? or ask for new appliance...
exit 1
fi

echo "New MIQ host IP: $NEW_MIQ_IP"
