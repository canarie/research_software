#!/bin/bash
#
#  Copyright 2014 - CANARIE Inc. All rights reserved
#
#  Synopsis: Runs the reference application server, kicks of the reference
#            application integration tests.
#
#
#  -------------------------------------------------------------------------------
#
#  Blob Hash: $Id$
#
#  -------------------------------------------------------------------------------
#
#  Redistribution and use in source and binary forms, with or without modification,
#  are permitted provided that the following conditions are met:
#
#  1. Redistributions of source code must retain the above copyright notice,
#     this list of conditions and the following disclaimer.
#
#  2. Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions and the following disclaimer in the documentation
#     and/or other materials provided with the distribution.
#
#  3. The name of the author may not be used to endorse or promote products
#     derived from this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY CANARIE Inc. "AS IS" AND ANY EXPRESS OR IMPLIED
#  WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
#  MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
#  EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#  EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
#  OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
#  INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
#  CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
#  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
#  POSSIBILITY OF SUCH DAMAGE.

echo ""
echo "UNIT TESTS"
echo "=========="

./manage.py test --with-xunit --xunit-file ../result_unit.xml
UNIT_SUCCESS=$?

echo ""
echo "INTEGRATION TESTS"
echo "=========="
rm db.sqlite3

# Recreate db from initial_data.json
./manage.py syncdb --noinput &> /dev/null

celery -q -A project worker -l info --statedb=./celery.worker.state &> /dev/null &


CELERY_PID=$!
CELERY_RESULT=$?

if [[ CELERY_RESULT -ne 0 ]]; then
    echo "Could not start celery, failing integration tests!"
    exit 1
fi

./manage.py runserver &> /dev/null &

MANAGE_PID=$!
MANAGE_RESULT=$?

if [[ MANAGE_RESULT -ne 0 ]]; then
    echo "Could not start manage.py, failing integration tests!"
    exit 1
fi

sleep 5
# perform integration tests
cd ../integration/python/
./run_tests.sh
INT_SUCCESS=$?


# shutdown django server here
ps auxww | grep 'runserver' | grep -v 'grep' | awk '{print $2}' | xargs kill &> /dev/null

# shutdown celery here
kill ${CELERY_PID} &> /dev/null

if (( $UNIT_SUCCESS == 0 && $INT_SUCCESS == 0 )); then
    exit 0
fi

exit 1
