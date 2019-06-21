"""
Copyright 2013 - CANARIE Inc. All rights reserved

Synopsis: Serializers to JSON for the database models

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

from rest_framework import serializers
from canarie_platform.models import Info, Statistic

import logging
log = logging.getLogger(__name__)

VALUE = 'usagename'


class IntAsTextField(serializers.Field):
    """ Saves an Int value as a writeable field.
    """
    def to_internal_value(self, obj):
        return "{0}".format(obj)
    
    def to_representation(self, obj):
        return int(obj)

class InfoSerializer(serializers.ModelSerializer):
    """ Helper class to serilaize the Info model to a Canarie Research
        Middleware API Stat response.
    """
    releaseTime = serializers.DateTimeField(source='release_time',
                                            format='%Y-%m-%dT%H:%M:%SZ')
    supportEmail = serializers.EmailField(source='support_email')
    researchSubject = serializers.EmailField(source='research_subject')
    tags = serializers.SerializerMethodField('as_array')

    class Meta:
        model = Info
        fields = ('name', 'synopsis', 'version', 'institution', 'releaseTime',
                  'supportEmail', 'researchSubject', 'tags')

    def as_array(self, obj):
        return obj.tags.split()


class StatSerializer(serializers.ModelSerializer):
    """ Helper class to serialize a generic Statistic to a Canarie Research
        Middleware API Stat response.
    """
    usagename = IntAsTextField(source='value')
    lastReset = serializers.DateTimeField(source='last_reset',
                                          read_only=True,
                                          format='%Y-%m-%dT%H:%M:%SZ')

    class Meta:
        model = Statistic
        fields = (VALUE, 'lastReset')


def convert(stat):
    """ Utility method to convert a Stat into the correct format for converting
        to a JSON response.
    """
    serializer = StatSerializer(stat)
    return swap_usage_name(serializer.data, stat.name)


def swap_usage_name(data, name):
    """ Utility method to swap out the serialized usage to the correct
        statistic name. This is needed due to the serilaizers not being able to
        dynamically set the name of an attribute. So the data is post processed
        to change the name of to the correct value for the response.
    """
    data[name] = data[VALUE]
    del data[VALUE]
    return data











