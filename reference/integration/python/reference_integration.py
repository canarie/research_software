#!/usr/bin/env python
"""
Copyright 2014 - CANARIE Inc. All rights reserved

Synopsis: Integration tests for the reference application

Blob Hash: $Id$

-------------------------------------------------------------------------------

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice,
   this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. The name of the author may not be used to endorse or promote products
   derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY CANARIE Inc. "AS IS" AND ANY EXPRESS OR IMPLIED
WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
"""

import unittest
import requests
import time
from httplib import OK

reference_url = 'http://localhost:8000'
headers = {'accept': 'application/json'}


class ReferenceIntegration(unittest.TestCase):
    def test_call_reference_service(self):
        ''' Check reference django server is up.

            Make a test call to the deployed server to ensure it is correctly
            configured
        '''
        try:
            r = requests.get("{}/admin/".format(reference_url),
                             headers=headers)

            self.assertEqual(r.status_code, OK,
                             'Unable to call reference service')
        except requests.ConnectionError:
            self.fail("Could not connect to host!")

    def test_poll_service(self):
        ''' Check that a call can be made through to the celery server and back
            to the service

            This test just works by checkiign that the intial call to the
            platform results in at least one call to the service
        '''
        try:
            r = requests.get('{}/reference/service/stats'.format(
                             reference_url), headers=headers)
            self.assertEqual(r.status_code, OK,
                             'Unable to call reference service')
            initial_result = r.json()['invocations']

            payload = {'start': 'start'}
            r = requests.post('{}/reference/platform/update'.format(
                              reference_url),
                              headers=headers, data=payload)
            self.assertEqual(r.status_code, OK,
                             'Unable to call reference platform')

            time.sleep(5)
            r = requests.get('{}/reference/service/stats'.format(
                             reference_url), headers=headers)
            self.assertEqual(r.status_code, OK,
                             'Unable to call reference service')
            self.assertGreater(r.json()['invocations'], initial_result,
                               'Stats should have incremented {} {}'.format(
                                    initial_result, r.json()['invocations']))

        except requests.ConnectionError:
            self.fail("Could not connect to host!")
