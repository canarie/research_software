"""
Copyright 2013 - CANARIE Inc. All rights reserved

Synopsis: Controls the site behaviour which includes:
          *  Showing the invocation counter with increment and reset
             functionality, available via the web view or REST
          *  Management of the service i.e. Updating 'info' data.
          *  Implementing the NEP-RPI API for monitoring

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

from datetime import datetime
import logging
from StringIO import StringIO

from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render
from django.utils.timezone import utc, now

from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from celery.result import AsyncResult

from canarie_platform.defaults import info as info_defaults
from canarie_platform.defaults import stats as stats_defaults
from canarie_platform.models import Info
from canarie_platform.models import Statistic
from canarie_platform.serializers import InfoSerializer, StatSerializer
from canarie_platform.serializers import convert
from canarie_platform.utility import get_poll
from canarie_platform.utility import get_configuration, MIN_SEC, MAX_SEC
from canarie_platform.utility import (SERVICE_URL, DOC_URL, RELEASE_NOTES_URL,
                                      SOURCE_URL, LICENCE_URL, PROVENANCE_URL,
                                      FACTSHEET_URL)
from canarie_platform.tasks import call_service

from util.shared import (NAME, SYNOPSIS, VERSION, INSTITUTION, RELEASE_TIME,
                         RELASE_TIME_JSON, SUPPORT_EMAIL, SUPPORT_EMAIL_JSON,
                         RESEARCH_SUBJECT, RESEARCH_SUBJECT_JSON, TAGS)

from util.shared import (get_field, num, validate_info_json,
                         FIELD_NOT_SET_ERROR, TIME_FORMAT, STATS_NAME,
                         STATS_VALUE, JSON_CONTENT)

import defaults

log = logging.getLogger(__name__)

template = 'canarie_platform/'
service_name = 'reference'


# Research Middleware API implementation views and methods
@api_view(['GET'])
def info(request):
    """ Return a JSON or HTML representaion of the latest info depending up on
        supplied accept header.
    """
    i = get_info()
    if request.META['HTTP_ACCEPT'] == JSON_CONTENT:
        serializer = InfoSerializer(i)
        return Response(data=serializer.data, content_type=JSON_CONTENT)

    return render(request, template+'info.html', {'info': i})


@api_view(['GET'])
def stats(request):
    """ Return a JSON or HTML representaion of the current statistics depending
        up on supplied accept header.
    """
    s = get_invocations()

    if request.META['HTTP_ACCEPT'] == JSON_CONTENT:
        return Response(data=convert(s), content_type=JSON_CONTENT)
    return render(request, template+'stats.html', {'stats': s})


def doc(request):
    """ Return a HTML representation of the current documentation """
    return HttpResponseRedirect(get_configuration(DOC_URL).value)


def release_notes(request):
    """ Return a HTML representation of the current releasenotes """
    return HttpResponseRedirect(get_configuration(RELEASE_NOTES_URL).value)


def support(request):
    """ Return a HTML representation of the current support """
    return render(request, template+'support.html')


def source(request):
    """ Return a HTML representation of the current source """
    return HttpResponseRedirect(get_configuration(SOURCE_URL).value)


def tryme(request):
    """ Redirect to the application """
    return HttpResponseRedirect(reverse('canarie_platform:app'))


def licence(request):
    """ Return a HTML representation of the current releasenotes """
    return HttpResponseRedirect(get_configuration(LICENCE_URL).value)


def provenance(request):
    """ Return a HTML representation of the current releasenotes """
    return HttpResponseRedirect(get_configuration(PROVENANCE_URL).value)


def factsheet(request):
    """ Return a HTML representation of the factsheet """
    return HttpResponseRedirect(get_configuration(FACTSHEET_URL).value)


# Reference Application views and methods
def app(request):
    """ The demonstration counter application """
    s = get_invocations()
    min_sec = get_configuration(MIN_SEC).value
    max_sec = get_configuration(MAX_SEC).value
    poll = get_poll(service_name)
    return render(request, template+'app.html', {'stats': s, 'min': min_sec,
                  'max': max_sec, 'running': poll_running(poll)})


@api_view(['POST'])
def update(request):
    """ React to the users input on the platforma application form.

        Options are:
            Start polling the reference service (increments usage count of
                the platform)
            Stop polling the reference service (increments usage count of
                the platform)
            Reset the count of interations with the platform
    """
    if check_for_param(request.POST, 'start'):
        start(request)
    elif check_for_param(request.POST, 'stop'):
        stop(request)
    elif check_for_param(request.POST, 'reset'):
        reset(request)

    return HttpResponseRedirect(reverse('canarie_platform:app'))


def check_for_param(param_list, param):
    """ Checks that a given param is set in the POST params
    """
    return param in param_list


@api_view(['PUT'])
def start(request):
    increment_counter(get_invocations())
    conf = get_configuration(SERVICE_URL)
    return create_running_response(start_poll(service_name, conf.value))


@api_view(['PUT'])
def stop(request):
    increment_counter(get_invocations())
    return create_running_response(stop_poll(service_name))


@api_view(['PUT'])
def reset(request):
    return Response(
        data=reset_counter(get_invocations()), content_type=JSON_CONTENT)


def create_running_response(running):
    status = dict()
    status['running'] = running
    log.info('running is: {0}'.format(running))
    log.info('status is: {0}'.format(status))
    return Response(status, content_type=JSON_CONTENT)


@transaction.atomic
def start_poll(name, url):
    """ Start polling the named service"""
    log.info('Starting polling the service')
    poll = get_poll(name)
    if poll.current_task_id:
        result = AsyncResult(poll.current_task_id)
        if not result.ready():
            log.info('Current task {0} is not finished'.format(
                     poll.current_task_id))
            return poll_running(poll)
        else:
            log.info('No poll continue')
    poll.url = url
    call = call_service.apply_async(args=[name])
    poll.current_task_id = call.task_id
    poll.save()
    return poll_running(poll)


def poll_running(poll):
    log.info(poll.current_task_id)
    return (poll.current_task_id is not None)


@transaction.atomic
def stop_poll(name):
    """ Stop polling the named service"""
    log.info('Stop service poll')
    poll = get_poll(name)
    poll.current_task_id = None
    poll.save()
    return poll_running(poll)


@transaction.atomic
def increment_counter(invocations):
    """ Increment the invocations statistic.

        The decorator @transaction.atomic wraps this method in an atomic
        transaction.

        See https://docs.djangoproject.com/en/1.6/topics/db/transactions
            /#controlling-transactions-explicitly
        for more details.
    """
    log.debug("Increment the counter")
    invocations.value = str(num(invocations.value) + 1)
    invocations.save()
    serializer = StatSerializer(invocations)
    return serializer.data


@transaction.atomic
def reset_counter(invocations):
    """ Reset the invocations statistic.

        The decorator @transaction.atomic wraps this method in an atomic
        transaction.

        See https://docs.djangoproject.com/en/1.6/topics/db/transactions
            /#controlling-transactions-explicitly
        for more details.
    """
    log.info("Reset the counter")
    invocations.value = '0'
    invocations.last_reset = now()
    invocations.save()
    return convert(invocations)


@api_view(['PUT'])
def setinfo(request):
    """ Set the info data """
    stream = StringIO(request.body)
    data = JSONParser().parse(stream)
    try:
        validate_info_json(defaults.EXPECTED_VALUES, data)
        info = parse_info_json(data)
        info.save()
        serializer = InfoSerializer(info)
        return Response(data=serializer.data, content_type=JSON_CONTENT)
    except ValueError as e:
        log.error('Invalid json data supplied {0}'.format(str(e)))
        log.error(data)
    return HttpResponseBadRequest('Invalid data')


# Utility methods

@transaction.atomic
def get_invocations():
    """ Get the invocations statistic from the db or seed with a new one if
        not there.

        As this method accesses the database and creates a new entry if needed
        the database access needs to be wrapped in a transaction so that
        another call to the same method does not create a duplicate record. The
        decorator @transaction.atomic wraps this method in an atomic
        transactions.
        See https://docs.djangoproject.com/en/1.6/topics/db/transactions
            /#controlling-transactions-explicitly
        for more details.
    """
    try:
        s = Statistic.objects.get(name=stats_defaults[STATS_NAME])
        log.debug('Got {0}'.format(str(s)))
    except ObjectDoesNotExist:
        s = Statistic(name=stats_defaults[STATS_NAME],
                      value=stats_defaults[STATS_VALUE],
                      last_reset=now())
        s.save()

    return s


@transaction.atomic
def get_info():
    """ Get the Info object from the db or seed with a new one if not there.

        As this method accesses the database and creates a new entry if needed
        the database access needs to be wrapped in a transaction so that
        another call to the same method does not create a duplicate record. The
        decorator @transaction.atomic wraps this method in an atomic
        transactions.
        See https://docs.djangoproject.com/en/1.6/topics/db/transactions
            /#controlling-transactions-explicitly
        for more details.
    """
    try:
        i = Info.objects.latest('pk')
    except ObjectDoesNotExist:
        i = Info(name=info_defaults[NAME],
                 synopsis=info_defaults[SYNOPSIS],
                 version=info_defaults[VERSION],
                 institution=info_defaults[INSTITUTION],
                 release_time=info_defaults[RELEASE_TIME],
                 support_email=info_defaults[SUPPORT_EMAIL],
                 research_subject=info_defaults[RESEARCH_SUBJECT],
                 tags=info_defaults[TAGS])
        i.save()
    return i


def parse_info_json(data):
    """ Create an Info object from JSON """
    info = Info()
    info.name = get_field(data, NAME)
    info.synopsis = get_field(data, SYNOPSIS)
    info.version = get_field(data, VERSION)
    info.institution = get_field(data, INSTITUTION)
    info.support_email = get_field(data, SUPPORT_EMAIL_JSON)
    info.research_subject = get_field(data, RESEARCH_SUBJECT_JSON)
    if TAGS in data and data.get(TAGS) and not isinstance(data.get(TAGS),
                                                          basestring):
        tags = data.get(TAGS)
        try:
            for index, tag in enumerate(tags):
                info.tags += tag
                if index < len(tags)-1:
                    info.tags += ' '
        except:
            raise ValueError(FIELD_NOT_SET_ERROR.format(TAGS))
    else:
        raise ValueError(FIELD_NOT_SET_ERROR.format(TAGS))

    if RELASE_TIME_JSON in data and data.get(RELASE_TIME_JSON):
        info.release_time = datetime.strptime(data.get(RELASE_TIME_JSON),
                                              TIME_FORMAT).replace(tzinfo=utc)
    else:
        raise ValueError(FIELD_NOT_SET_ERROR.format(RELASE_TIME_JSON))

    return info
