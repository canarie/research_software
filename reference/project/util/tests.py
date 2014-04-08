"""
Copyright 2014 - CANARIE Inc. All rights reserved

Tests for utility methods used in the reference application

Blob Hash: $Id$

-------------------------------------------------------------------------------

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

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
from django.test import TestCase

from shared import validate_info_json, get_field, num

data = {'key1': 'val1', 'key2': 'val2'}


class SharedUtilsTests(TestCase):
    def test_num_int(self):
        self.assertEquals(num('3'), 3)

    def test_num_float(self):
        self.assertEquals(num('3.5'), 3.5)

    def test_bad_num(self):
        with self.assertRaises(ValueError):
            num('string')

    def test_get_field(self):
        self.assertEqual(get_field(data, 'key1'), 'val1')

    def test_get_field_not_there(self):
        with self.assertRaises(ValueError):
            get_field(data, 'key3')

    def test_validate_info_json(self):
        self.assertTrue(validate_info_json(set(('key1', 'key2')), data))

    def test_validate_info_json_bad_data(self):
        with self.assertRaises(ValueError):
            validate_info_json(set(('key3', 'key2')), data)
