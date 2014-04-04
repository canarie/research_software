"""
Copyright 2014 - CANARIE Inc. All rights reserved

Synopsis: Contains the default values used in teh Service

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

from util.shared import (NAME, SYNOPSIS, VERSION, INSTITUTION,
                         RELASE_TIME_JSON, RESEARCH_SUBJECT_JSON,
                         SUPPORT_EMAIL_JSON, TAGS)

"""
    Defualt values for a new Info entry to the database if one if not already
    present
"""
info = {'name': 'Reference Service',
        'synopsis': 'The Reference Service implementation of the NEP-RPI API revision 6',
        'version': '2.0',
        'institution': 'CANARIE',
        'release_time': now(),
        'support_email': 'support@science.canarie.ca',
        'category': 'Other',
        'research_subject': 'Software and development',
        'tags': 'CANARIE RPI reference'}

"""
    Default values for the Stat entry to the database
"""
stats = {'name': 'invocations',
         'value': '0'}

EXPECTED_VALUES = set((NAME, SYNOPSIS, VERSION, INSTITUTION, RELASE_TIME_JSON,
                       RESEARCH_SUBJECT_JSON, SUPPORT_EMAIL_JSON, TAGS))
