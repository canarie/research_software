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
    
USAGE_NAME = '# invocations'

valid_info_json_base = '{"name":"n", \
                 "version":"v", \
                 "synopsis":"s", \
                 "institution":"i", \
                 "releaseTime":"2014-01-07T18:50:36Z",\
                 "researchSubject":"rs",\
                 "supportEmail":"e@example.com",\
                 "category":"o",'

# This file contains unit tests for the methods in the view.py file. 
# For simplicity all the tests are in one test class
class ViewUtilsTests(TestCase):
    
    def setUp(self):
        self.factory = APIRequestFactory()
        
    def test_get_field_value(self):
        info = Info()
        view.get_field(get_as_json('{"new":"val"}'), 'new')
    
    def test_get_field_value_not_in_info(self):
        info = Info()
        with self.assertRaises(ValueError):
            view.get_field(get_as_json('{"new":"val"}'), 'old')
        
    # Tests for the parse_json method 
    def test_parse_info_json(self):
        json = valid_info_json_base + '"tags":["TAG1","TAG2", "TAG3"]}'
        info = view.parse_info_json(get_as_json(json))
        self.assertEquals(info.name, 'n', 'Info should be populated')
        self.assertEquals(info.tags, 'TAG1 TAG2 TAG3', 'Info tags should be populated')
    
    def test_parse_info_json_no_tags(self):
        json = valid_info_json_base + '"tags":[]}'
        with self.assertRaises(ValueError):
            info = view.parse_info_json(get_as_json(json))
            
    def test_parse_info_json_tags_full_string(self):
        json = valid_info_json_base + '"tags":"tag tag tag"}'
        with self.assertRaises(ValueError):
            info = view.parse_info_json(get_as_json(json))
            
    def test_parse_info_json_tags_empty_string(self):
        json = valid_info_json_base + '"tags":""}'
        with self.assertRaises(ValueError):
            info = view.parse_info_json(get_as_json(json))
        
        
    def test_parse_info_json_missing_element(self):
        json = '{"version":"aversion", \
                 "synopsis":"asynopsis", \
                 "institution":"ainstitution", \
                 "releaseTime":"2014-01-07T18:50:36Z"}'
        with self.assertRaises(ValueError):
            view.parse_info_json(get_as_json(json))
        
    def test_parse_info_json_missing_time(self):
        json = '{"name":"aname", \
                 "version":"aversion", \
                 "synopsis":"asynopsis", \
                 "institution":"ainstitution", \
                 "researchSubject":"rs", \
                 "supportEmail":"e@example.com", \
                 "category":"o", \
                 "tags":["TAG1","TAG2", "TAG3"]}'
        with self.assertRaises(ValueError):
            info = view.parse_info_json(get_as_json(json))
 
    # Tests for the validate_json method 
    def test_validate_info_json(self):
        json = valid_info_json_base + '"tags":["TAG1","TAG2"]}'
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
        info.name = 'n'
        info.synopsis = 's'
        info.version = 'v'
        info.institution = 'i'
        info.release_time = now()
        info.support_email = 'e'
        info.research_subject = 'rs'
        info.category = 'o'
        info.tags = 'TAG1 TAG2'
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
        inv = Statistic(name=USAGE_NAME, value='5', last_reset=now())
        inv.save()
        
        self.assertEqual(inv, view.get_invocations(), 
                         'Invocations statistic should be retrived from the database')
        
    def test_get_invocations_non_existing(self):
        # check the db is actually clean
        with self.assertRaises(ObjectDoesNotExist):
            Statistic.objects.get(name=USAGE_NAME)
            
        inv = view.get_invocations()
        self.assertEqual(inv.name, USAGE_NAME, 
                         'The invocations entry should have been created')
        self.assertEqual(inv.value, '0', 
                         'The invocations value should have been created')
        
    # Tests for the set_info functionality
    def test_set_info(self):
        data = valid_info_json_base + '"tags":["t1","t2"]}'
        
        with self.assertRaises(ObjectDoesNotExist):
            Info.objects.latest('pk')
            
        request = self.factory.put('/setinfo/', data, content_type='application/json')
        
        response = view.setinfo(request)
        response.render()
        self.assertEqual(response.status_code, 200)
        
        info = Info.objects.latest('pk')
        self.assertEquals(info.name, 'n')
        self.assertEquals(info.synopsis, 's')
        self.assertEquals(info.version, 'v')
        self.assertEquals(info.institution, 'i')
        self.assertTrue(info.release_time)
        self.assertEquals(info.support_email, 'e@example.com')
        self.assertEquals(info.research_subject, 'rs')
        self.assertEquals(info.category, 'o')
        self.assertEquals(info.tags, 't1 t2')
        
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
        inv = Statistic(name=USAGE_NAME, value='5', last_reset=init_time) 
        inv.save()
        
        data = view.reset_counter(inv)
        inv = Statistic.objects.get(name=USAGE_NAME)
        
        self.assertEqual(inv.value, '0', 'Should have been reset')
        self.assertTrue(inv.last_reset > init_time, 'Time should have been reset')
        
    # Test for increment_counter method
    def test_increment_counter(self):
        inv = Statistic(name=USAGE_NAME, value='5', last_reset=now()) 
        inv.save()
        
        data = view.increment_counter(inv)
        self.assertEqual(inv.value, '6')
        
        
        
   
        
