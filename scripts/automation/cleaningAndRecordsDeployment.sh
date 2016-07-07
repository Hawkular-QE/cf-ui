#!/bin/sh
echo "Cleaning..."

# stop Docker container
# Sprout appliance is recreated when source branch is origin/master (that happens at least once a day)

echo "Tests records deployment..."

rm -rf html_comment.properties
touch html_comment.properties
mkdir /var/www/html/records/${BUILD_ID}/
cp ${WORKSPACE}/records/*.flv /var/www/html/records/${BUILD_ID}/

echo -n "HTML_SNIPPET = Gif records:<br>" > html_comment.properties

FLV_FILES=/var/www/html/records/${BUILD_ID}/*.flv
for FLV_FILE in $FLV_FILES ; do
if [ -f $FLV_FILE ]; then
FLVBASENAME=$(basename $FLV_FILE)
echo -n " - [${FLVBASENAME%.*}.flv](http://$(hostname -i)/records/${BUILD_ID}/${FLVBASENAME%.*}.flv) <br>" >> html_comment.properties
fi
done
