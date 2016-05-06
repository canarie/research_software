#!/bin/bash

nosetests --with-xunit -v -s --xunit-file=/workspace/result_webtest.xml --where=/scripts/ --tests=main.py
NOSE_RESULT=$?

exit ${NOSE_RESULT}
