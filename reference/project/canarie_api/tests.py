"""
Copyright 2013 - CANARIE Inc. All rights reserved

Synopsis: Unit tests

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
from StringIO import StringIO

import datetime
import pytz

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest
from django.test import TestCase

from rest_framework.parsers import JSONParser
from rest_framework.test import APIClient
from rest_framework.test import APIRequestFactory
from django.utils.timezone import utc, now


from canarie_api import views as view
from canarie_api.models import Info, Statistic

def get_as_json(text):
    return JSONParser().parse(StringIO(text))

# This file containes unit tests for the methods in the view.py file. 
# For simplicity all the tests are in one test class
class ViewUtilsTests(TestCase):
    
    def setUp(self):
        self.factory = APIRequestFactory()
    
    # Tests for the write_field method
    def test_write_field_good(self):
        info = Info()
        self.assertTrue(not info.name, 'Name should not be set')
        view.write_field(info, "name", get_as_json('{"name":"aname"}'))
        self.assertEquals(info.name, 'aname', 'Name should be set')
        
    def test_write_field_value_not_in_info(self):
        info = Info()
        self.assertRaises(ValueError, 
                          view.write_field(info, "new", 
                                           get_as_json('{"new":"val"}')), 
                          'Should raise ValueError')
        
    def test_write_field_value_not_in_data(self):
        info = Info()
        self.assertRaises(ValueError, view.write_field(info, "name", 
                          get_as_json('{"new":"val"}')), 
                          'Should raise ValueError')
    
    # Tests for the parse_json method 
    def test_parse_info_json(self):
        json = '{"name":"aname", \
                 "version":"aversion", \
                 "synopsis":"asynopsis", \
                 "institution":"ainstitution", \
                 "releaseTime":"2014-01-07T18:50:36Z"}'
        info = view.parse_info_json(get_as_json(json))
        self.assertEquals(info.name, 'aname', 'Info should be populated')
        
    def test_parse_info_json_missing_element(self):
        json = '{"version":"aversion", \
                 "synopsis":"asynopsis", \
                 "institution":"ainstitution", \
                 "releaseTime":"2014-01-07T18:50:36Z"}'
        info = view.parse_info_json(get_as_json(json))
        self.assertEquals(info.name, '', 'Name should be empty')
        
    def test_parse_info_json_missing_time(self):
        json = '{"name":"aname", \
                 "version":"aversion", \
                 "synopsis":"asynopsis", \
                 "institution":"ainstitution"}'
        info = view.parse_info_json(get_as_json(json))
        self.assertEquals(info.release_time, '', 'release_time should be empty')
     
    # Tests for the validate_json method 
    def test_validate_info_json(self):
        json = '{"name":"aname", \
                 "version":"aversion", \
                 "synopsis":"asynopsis", \
                 "institution":"ainstitution", \
                 "releaseTime":"2014-01-07T18:50:36Z"}'
        self.assertTrue(view.validate_info_json(get_as_json(json)), 
                        'JSON should validate')
        
    def test_validate_info_json_incomplete_data(self):
        json = '{"version":"aversion", \
                 "synopsis":"asynopsis", \
                 "institution":"ainstitution", \
                 "releaseTime":"2014-01-07T18:50:36Z"}'
        with self.assertRaises(ValueError):
            view.validate_info_json(get_as_json(json))
    
    
    # Tests for the get_info method
    def test_get_info_existing(self):
        info = Info()
        info.name = 'aname'
        info.synopsis = 'synopsis'
        info.version = 'version'
        info.institution = 'institution'
        info.release_time = now()
        info.save()
        
        self.assertEqual(info, view.get_info(), 
                         'Info object should be retrived from the database')
        
    def test_get_info_non_existing(self):
        # check the db is actually clean
        with self.assertRaises(ObjectDoesNotExist):
            Info.objects.latest('pk')
            
        info = view.get_info()
        self.assertEqual(info.name, 'Reference Service', 
                         'The Reference entry should have been created')
    
    # Tests for the get_invocations method    
    def test_get_invocations(self):
        inv = Statistic(name='invocations', value='5', last_reset=now())
        inv.save()
        
        self.assertEqual(inv, view.get_invocations(), 
                         'Invocations statistic should be retrived from the database')
        
    def test_get_invocations_non_existing(self):
        # check the db is actually clean
        with self.assertRaises(ObjectDoesNotExist):
            Statistic.objects.get(name='invocations')
            
        inv = view.get_invocations()
        self.assertEqual(inv.name, 'invocations', 
                         'The invocations entry should have been created')
        self.assertEqual(inv.value, '0', 
                         'The invocations value should have been created')
        
    # Tests for the set_info functionality
    def test_set_info(self):
        data = '{"name":"aname", \
                 "version":"aversion", \
                 "synopsis":"asynopsis", \
                 "institution":"ainstitution", \
                 "releaseTime":"2014-01-07T18:50:36Z"}'
        
        with self.assertRaises(ObjectDoesNotExist):
            Info.objects.latest('pk')
            
        request = self.factory.put('/setinfo/', data, content_type='application/json')
        
        response = view.setinfo(request)
        response.render()
        self.assertEqual(response.status_code, 200)
        
        info = Info.objects.latest('pk')
        self.assertEquals(info.name, 'aname')
        
    def test_set_info_missing_field(self):
        data = '{"name":"aname", \
                 "synopsis":"asynopsis", \
                 "institution":"ainstitution", \
                 "releaseTime":"2014-01-07T18:50:36Z"}'
        
        with self.assertRaises(ObjectDoesNotExist):
            Info.objects.latest('pk')
            
        request = self.factory.put('/setinfo/', data, content_type='application/json')
        
        response = view.setinfo(request)
        self.assertEqual(response.status_code, 400)
        
        with self.assertRaises(ObjectDoesNotExist):
            Info.objects.latest('pk')
    
    # Test for reset_counter method
    def test_reset_counter(self):
        init_time = now() - datetime.timedelta(days=1)
        inv = Statistic(name='invocations', value='5', last_reset=init_time) 
        inv.save()
        
        data = view.reset_counter(inv)
        inv = Statistic.objects.get(name='invocations')
        
        self.assertEqual(inv.value, '0', 'Should have been reset')
        self.assertTrue(inv.last_reset > init_time, 'Time should have been reset')
        
    # Test for increment_counter method
    def test_increment_counter(self):
        inv = Statistic(name='invocations', value='5', last_reset=now()) 
        inv.save()
        
        data = view.increment_counter(inv)
        self.assertEqual(inv.value, '6')
        
        
        
   
        
