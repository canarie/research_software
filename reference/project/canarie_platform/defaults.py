"""
Copyright 2014 - CANARIE Inc. All rights reserved

Synopsis: Contains the default values for the Platform

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
from django.utils.timezone import now

from util import shared

# This is the defauls value and should be updated to the correct url for the
# system in the database Configuration table
SERVICE_URL = ('http://127.0.0.1:8000/reference/service/add')

"""
    Defualt values for a new Info entry to the database if one if not already
    present
"""
info = {'name': 'Reference Platform (INSERT LOCATION)',
        'synopsis': ('The reference implementation of the NEP-RPI API for '
                     'platforms revision 2'),
        'version': '2.0',
        'institution': 'CANARIE',
        'release_time': now(),
        'support_email': 'support@science.canarie.ca',
        'research_subject': 'Software and development',
        'tags': 'CANARIE RPI reference platform'}

""" Default values for the Stat entry to the database
"""
stats = {'name': 'interactions',
         'value': '0'}

EXPECTED_VALUES = set((shared.NAME, shared.SYNOPSIS, shared.VERSION,
                      shared.INSTITUTION, shared.RELASE_TIME_JSON,
                      shared.RESEARCH_SUBJECT_JSON, shared.SUPPORT_EMAIL_JSON,
                      shared.TAGS))
