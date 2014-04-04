"""
Copyright 2014 - CANARIE Inc. All rights reserved

Synopsis: Celery (http://www.celeryproject.org/) tasks for the platform

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
import random
from httplib import OK

import requests

from canarie_platform.utility import get_poll, update_task_id
from celery import shared_task

log = logging.getLogger(__name__)


@shared_task
def call_service(name):
    """ A Celery worker task (see http://www.celeryproject.org/) to perform a
        scheduled poll to the reference service.
    """
    log.info('Worker task called')
    next_id = None
    poll = get_poll(name)
    log.info('Expected {0}, current {1}'.format(poll.current_task_id,
             call_service.request.id))
    if poll.current_task_id == call_service.request.id:
        log.info('Calling service at {0}'.format(poll.url))
        r = requests.put(poll.url)
        if r.status_code is OK:
            log.info('Good response from service')
        else:
            log.error('Unable to call counter service: {0}'.format(r.reason))

        interval = random.randint(poll.min_sec, poll.max_sec)
        log.info('Continue running and schedule next poll for {0} seconds'.
                 format(interval))
        next_id = call_service.apply_async(args=[name], countdown=interval)
    else:
        log.info('Not running just finish (current expected task is is not '
                 'this tasks id)')
    update_task_id(name, next_id)
