"""
Copyright 2014 - CANARIE Inc. All rights reserved

Synopsis: Platform Database Schema

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

from django.db import models
from util.shared import TEXT_FIELD_SIZE


class Info(models.Model):
    """ Defines the Info table in the database to store the data required by
        the Canarie Research Middleware API.
    """
    name = models.CharField(max_length=TEXT_FIELD_SIZE, blank=False)
    synopsis = models.TextField(blank=False)
    version = models.CharField(max_length=TEXT_FIELD_SIZE, blank=False)
    institution = models.CharField(max_length=TEXT_FIELD_SIZE, blank=False)
    release_time = models.DateTimeField(blank=False)
    support_email = models.EmailField(max_length=TEXT_FIELD_SIZE, blank=False)
    research_subject = models.CharField(max_length=TEXT_FIELD_SIZE,
                                        blank=False)
    tags = models.TextField(blank=False)

    def __str__(self):
        return ('name:{0}'.format(self.name))


class Statistic(models.Model):
    """ Defines a generic statistic that can be stored in the database """
    name = models.CharField(max_length=TEXT_FIELD_SIZE, blank=False)
    value = models.CharField(max_length=TEXT_FIELD_SIZE, blank=False)
    last_reset = models.DateTimeField(blank=False)

    def __str__(self):
        return ('name:{0}, value:{1}, last_reset:{2}'.format(
                self.name, self.value, self.last_reset))


class Poll(models.Model):
    """ Used to keep track of polling state to a service """
    name = models.CharField(max_length=TEXT_FIELD_SIZE, blank=False,
                            unique=True)
    min_sec = models.IntegerField(blank=False)
    max_sec = models.IntegerField(blank=False)
    url = models.TextField()
    current_task_id = models.TextField(blank=True, null=True)

    def __str__(self):
        return "Poll for {0} ({1})".format(self.name, self.current_task_id)


class Configuration(models.Model):
    service_url = models.TextField(blank=False)

    def __str__(self):
        return 'Configuration details'
