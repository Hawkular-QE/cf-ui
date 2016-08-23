#!/bin/sh

# export dispaly port to let browser know where it should open
export DISPLAY=:${DISPLAY_PORT}

# new Execute shell = new activation of virtualenv
source .cf-ui/bin/activate

echo "Starting tests..."
for TEST_FILE in $TEST_FILES ; do
echo $TEST_FILE

# for debug purposes
if [ "$RUN_TESTS" = true ] ; then

# all tests should be independent so order of testing does not matter
python -m pytest -s $TEST_FILE --junitxml=polarion-output.xml --ignore=tests/framework # | tee -a ${WORKSPACE}/pytest.log

# stop recording
if ["$RECORD_TESTS" = true] ; then
    pkill -SIGINT -f flvrec.py
fi

else
echo "Skipping tests because of build parameter RUN_TESTS=False"
fi
done
