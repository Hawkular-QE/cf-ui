#!/bin/sh
n=0
THISFILE=$(readlink -f -- "${0}")
THISDIR=${THISFILE%/*}

${THISDIR}/requestNewUpstreamSproutAppliance.sh
until [[ $? -eq 0 ]]; do
n=$[$n+1]
if [ $n -eq 5 ]; then
   exit 1;
fi
echo "Rerunning  .${THISDIR}/requestNewUpstreamSproutAppliance.sh for $n-th time"
${THISDIR}/requestNewUpstreamSproutAppliance.sh
done
