#!/bin/bash

echo "Running tests"
nosetests --with-xunit -v -s --xunit-file=/workspace/result.xml --where=/scripts/ --tests=test.py
NOSE_RESULT=$?

echo "Tests complete"

exit ${NOSE_RESULT}
