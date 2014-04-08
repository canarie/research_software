"""
Copyright 2014 - CANARIE Inc. All rights reserved

Synopsis: Utility methods shared in the reference application

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

import exceptions

TEXT_FIELD_SIZE = 254

TIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
STATS_NAME = 'name'
STATS_VALUE = 'value'
JSON_CONTENT = 'application/json'

NAME = 'name'
SYNOPSIS = 'synopsis'
VERSION = 'version'
INSTITUTION = 'institution'
RELEASE_TIME = 'release_time'
RELASE_TIME_JSON = 'releaseTime'
SUPPORT_EMAIL = 'support_email'
SUPPORT_EMAIL_JSON = 'supportEmail'
CATEGORY = 'category'
RESEARCH_SUBJECT = 'research_subject'
RESEARCH_SUBJECT_JSON = 'researchSubject'
TAGS = 'tags'

FIELD_NOT_SET_ERROR = 'Field {0} not set'


def validate_info_json(expected, data):
    """ Validate that all the required fields in the input are present.

    """
    if expected <= set(data):
        return True
    raise ValueError('Invalid content')


def get_field(data, field_name):
    """ Get a field from the json data and return it. If it is not thair raise
        an error

    """
    if field_name in data and data.get(field_name):
        return data.get(field_name)

    raise ValueError(FIELD_NOT_SET_ERROR.format(field_name))


def num(s):
    """ Parse a number from a string.

    """
    try:
        return int(s)
    except exceptions.ValueError:
        return float(s)
