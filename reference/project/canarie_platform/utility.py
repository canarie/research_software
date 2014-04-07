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
from canarie_platform.defaults import SERVICE_URL

log = logging.getLogger(__name__)

MIN_SEC_DEFAULT = 1
MAX_SEC_DEFAULT = 10


@transaction.atomic
def is_running(name):
    poll = get_poll(name)
    return poll.current_task_id is not None


@transaction.atomic
def get_poll(name):
    """ Get the named Poll
    """
    try:
        poll = Poll.objects.get(name=name)
    except ObjectDoesNotExist:
        poll = Poll(name=name, min_sec=MIN_SEC_DEFAULT,
                    max_sec=MAX_SEC_DEFAULT)
        poll.save()
    return poll


@transaction.atomic
def update_task_id(name, id):
    poll = get_poll(name)
    poll.current_task_id = id
    poll.save()


@transaction.atomic
def get_configuration():
    try:
        conf = Configuration.objects.latest('pk')
    except ObjectDoesNotExist:
        conf = Configuration(service_url=SERVICE_URL)
        conf.save()

    return conf
