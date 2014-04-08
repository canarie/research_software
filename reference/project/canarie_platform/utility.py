"""
Copyright 2014 - CANARIE Inc. All rights reserved

Synopsis: Utility methods used in the Platform

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

import logging

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from canarie_platform.models import Poll, Configuration

log = logging.getLogger(__name__)

SERVICE_URL = 'service_url'
DOC_URL = 'doc_url'
RELEASE_NOTES_URL = 'release_notes_url'
SOURCE_URL = 'source_url'
LICENCE_URL = 'licence_url'
PROVENANCE_URL = 'provenance_url'
FACTSHEET_URL = 'factsheet_url'
MIN_SEC = 'min_sec'
MAX_SEC = 'max_sec'
SUPPORT_EMAIL = 'support_email'

DEFAULT_CONFIG = {
    DOC_URL: ('https://github.com/canarie/research_software/blob/master'
              '/reference/ReferenceServiceAndPlatformDesignNote.docx'),
    RELEASE_NOTES_URL: ('https://github.com/canarie/research_software/blob'
                        '/master/reference/release_notes.md'),
    SOURCE_URL: ('https://github.com/canarie/research_software/tree/master'
                 '/reference'),
    LICENCE_URL: ('https://github.com/canarie/research_software/blob/master'
                  '/reference/licence.md'),
    PROVENANCE_URL: ('https://github.com/canarie/research_software/blob/master'
                     '/reference/provenance.md'),
    FACTSHEET_URL: ('https://github.com/canarie/research_software/blob/master'
                    '/reference/provenance.md'),
    SERVICE_URL: ('http://127.0.0.1:8000/reference/service/add'),
    MIN_SEC: '1',
    MAX_SEC: '10'
    }


@transaction.atomic
def is_running(name):
    poll = get_poll(name)
    return poll.current_task_id is not None


@transaction.atomic
def get_poll(name):
    """ Get the named Poll """
    try:
        poll = Poll.objects.get(name=name)
    except ObjectDoesNotExist:
        log.info('No poll exists, creating default')
        poll = Poll(name=name)
        poll.save()
    return poll


@transaction.atomic
def remove_poll(name):
    """ Remove the poll from the db """
    try:
        poll = Poll.objects.get(name=name)
        poll.delete()
    except ObjectDoesNotExist:
        log.warning('No poll named {} to delete'.format(name))


@transaction.atomic
def update_task_id(name, id):
    poll = get_poll(name)
    poll.current_task_id = id
    poll.save()


@transaction.atomic
def get_configuration(name):
    try:
        if Configuration.objects.count() is 0:
            init_config()
        conf = Configuration.objects.get(name=name)
    except ObjectDoesNotExist:
        log.error('{} not in Configuration'.format(name))
        return None

    return conf


def init_config():
    log.info('Initialising config')
    for key in DEFAULT_CONFIG:
        conf = Configuration(name=key, value=DEFAULT_CONFIG[key])
        conf.save()


