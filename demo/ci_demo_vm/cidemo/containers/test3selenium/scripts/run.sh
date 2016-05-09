#!/bin/bash

echo "Waiting for web server to initialize"
dockerize -timeout 60s -wait http://web:80

echo "Running tests"
nosetests --with-xunit -v -s --xunit-file=/workspace/result_webtest.xml --where=/scripts/ --tests=main.py
NOSE_RESULT=$?

echo "Tests complete"

exit ${NOSE_RESULT}
