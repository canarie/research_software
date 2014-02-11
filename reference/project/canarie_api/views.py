"""
Copyright 2013 - CANARIE Inc. All rights reserved

Synopsis: Controls the site behaviour which includes:
          *  Showing the invocation counter with increment and reset 
             functionality, available via the web view or REST
          *  Management of the service i.e. Updating 'info' data.  
          *  Implementing the NEP-RPI API for monitoring

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

from datetime import datetime
import logging
from StringIO import StringIO

from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.utils.timezone import utc, now
from django.db import IntegrityError, transaction


from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from canarie_api.models import Info
from canarie_api.models import Statistic
from canarie_api.serializers import InfoSerializer, StatSerializer
from canarie_api.serializers import convert

from canarie_api.defaults import info as info_defaults
from canarie_api.defaults import stats as stats_defaults

log = logging.getLogger(__name__)

template = 'canarie_api/'

JSON_CONTENT = 'application/json'

name = 'name'
invocations = 'invocations'
synopsis = 'synopsis'

def index(request) : 
    return HttpResponse("Index page.")


# Research Middleware API implementation views and methods

@api_view(['GET'])
def info(request) :
    """ Return a JSON or HTML representaion of the latest info depending up on 
        supplied accept header.
    
    """
    i = get_info()
    if request.META['HTTP_ACCEPT'] == JSON_CONTENT:
        serializer = InfoSerializer(i)
        return Response(data=serializer.data, content_type=JSON_CONTENT)	
  
    return render(request, template+'info.html', {'info':i}) 

@api_view(['GET'])
def stats(request) :
    """ Return a JSON or HTML representaion of the current statistics depending 
        up on supplied accept header.
    
    """
    s = get_invocations()
    if request.META['HTTP_ACCEPT'] == JSON_CONTENT:
        return Response(data=convert(s), content_type=JSON_CONTENT)
    return render(request, template+'stats.html', {'stats':s})  

def doc(request) :
    """ Return a HTML representation of the current documentation 
    
    """
    return HttpResponseRedirect('https://github.com/canarie/research_software/blob/master/reference/ReferenceServiceDesignNote.docx')

def release_notes(request):
    """ Return a HTML representation of the current releasenotes 
    
    """
    return HttpResponseRedirect('https://github.com/canarie/research_software/blob/master/reference/release_notes.md')

def support(request): 
    """ Return a HTML representation of the current support 
    
    """
    return render(request, template+'support.html')

def source(request):
    """ Return a HTML representation of the current source 
    
    """
    return HttpResponseRedirect('https://github.com/canarie/research_software/tree/master/reference')

def tryme(request): 
    """ Redirect to the application 
    
    """
    return HttpResponseRedirect(reverse('canarie:app'))
    
def licence(request):
    """ Return a HTML representation of the current releasenotes 
    
    """
    return HttpResponseRedirect('https://github.com/canarie/research_software/blob/master/reference/licence.md')
    
def provenance(request):
    """ Return a HTML representation of the current releasenotes 
    
    """
    return HttpResponseRedirect('https://github.com/canarie/research_software/blob/master/reference/provenance.md')


# Reference Application views and methods
# A simple counter application

def app(request):
    """ The demonstration counter application
    
    """
    s = get_invocations()
    return render(request, template+'app.html', {'stats':s})

def update(request):
    """ Manage and display updates to the application invocation counter 
    
    """
    if 'add' in request.POST:
        increment_counter(get_invocations())
    elif 'reset' in request.POST : 
        reset_counter(get_invocations())
    return HttpResponseRedirect(reverse('canarie:app'))

@api_view(['PUT'])
def add(request):
    """ REST call to add to the counter
         
    """
    return Response(
        data=increment_counter(get_invocations()), content_type=JSON_CONTENT)
    
@api_view(['PUT'])
def reset(request):
    """ REST call to reset the counter
        
    """
    return Response(
        data=reset_counter(get_invocations()), content_type=JSON_CONTENT)

@transaction.atomic
def increment_counter(invocations):
    """ Increment the invocations statistic. 
    
    """
    log.debug("Increment the counter")
    invocations.value = str(num(invocations.value) + 1)
    invocations.save()
    serializer = StatSerializer(invocations) 
    return serializer.data   

@transaction.atomic
def reset_counter(invocations):
    """ Reset the invocations statistic. 
    
    """
    log.debug("Reset the counter")
    invocations.value = '0'
    invocations.last_reset = now()
    invocations.save()
    serializer = StatSerializer(invocations) 
    return serializer.data

@api_view(['PUT'])  
def setinfo(request):
    """ Set the info data. 
    
    """
    stream = StringIO(request.body)
    data = JSONParser().parse(stream)
    try:
        validate_info_json(data)
        info = parse_info_json(data)
        info.save()
        serializer = InfoSerializer(info)
        return Response(data=serializer.data, content_type=JSON_CONTENT)
    except ValueError as e:
        log.error('Invalid json data supplied {0}'.format(str(e)))  
    return HttpResponseBadRequest('Invalid data')	    
  

# Utility methods
@transaction.atomic
def get_invocations():
    """ Get the invocations statistic from the db or seed with a new one if 
        not there.
    
    """
    try:
        s = Statistic.objects.get(name=stats_defaults['name'])
        log.debug('Got {0}'.format(str(s)))
    except ObjectDoesNotExist:
        s = Statistic(name=stats_defaults['name'], 
                      value=stats_defaults['value'], 
                      last_reset=now())
        log.debug('Created {0}'.format(str(s)))
    return s

@transaction.atomic
def get_info():
    """ Get the Info object from the db or seed with a new one if not there.
    
    """
    try: 
        s = Info.objects.latest('pk')
    except ObjectDoesNotExist:
        s = Info(name=info_defaults['name'], 
                 synopsis=info_defaults['synopsis'], 
                 version=info_defaults['version'], 
                 institution=info_defaults['institution'], 
                 release_time=info_defaults['release_time'],
                 support_email=info_defaults['support_email'],
                 category=info_defaults['category'],
                 research_subject=info_defaults['research_subject'],
                 tags=info_defaults['tags'])
        s.save()
    return s
    
def validate_info_json(data):
    """ Validate that all the required fields in the input are present.
    
    """
    if set(('name', 'synopsis', 'version', 'institution', 'releaseTime', 
            'researchSubject', 'supportEmail', 'category', 'tags')) <= set(data):
        return True
    raise ValueError('Invalid content')
  
def parse_info_json(data):
    """ Create an Info object from JSON. 
    
    """
    info = Info()
    write_field(info, 'name', data)
    write_field(info, 'synopsis', data)
    write_field(info, 'version', data)
    write_field(info, 'institution', data)
    write_field(info, 'support_email', data)
    write_field(info, 'category', data)
    write_field(info, 'research_subject', data)
    if 'tags' in data and data.get('tags'):    
        tags = data.get('tags')
        try:
            for index, tag in enumerate(tags):
                info.tags += tag 
                if index < len(tags)-1:
                    info.tags += ' '
        except:
            info.tags = ''
    else:
        info.tags = ''        
        
    if 'releaseTime' in data and data.get('releaseTime'):
        info.release_time = datetime.strptime(
                                data.get('releaseTime'),
                                '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=utc)
    else:
        info.release_time = ''
    
    return info
  	  
def write_field(info, field, data):
    """ Write a field to an Info object from JSON data. 
    
    """
    try:
        value = data.get(field) if data.get(field) else ''
        setattr(info, field, value)
    except :
        raise ValueError('{0} not set'.format(field))

def num (s):
    """ Parse a number from a string. 
    
    """
    try:
        return int(s)
    except exceptions.ValueError:
        return float(s)
    

