#!/bin/sh

EXIT_STATUS=0

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
        if [ $? -eq 0 ]; then
            echo "Test Success."
        else
            echo "Test Failed."
            EXIT_STATUS=1
        fi

        # stop recording
        echo "RECORD_TESTS: $RECORD_TESTS"
        if [ "$RECORD_TESTS" == "True" ] ; then
            pkill -SIGINT -f flvrec.py
        fi

    else
        echo "Skipping tests because of build parameter RUN_TESTS=False"
    fi
done
exit $EXIT_STATUS
