#!/bin/bash

# Copyright 2016 - CANARIE Inc. All rights reserved
#
# Synopsis: Demo elasticsearch container using in memory storage
#
# Blob Hash: $Id$
#
# -------------------------------------------------------------------------------
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# 3. The name of the author may not be used to endorse or promote products
# derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY CANARIE Inc. "AS IS" AND ANY EXPRESS OR IMPLIED
# WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
# EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#

FROM centos:6.6
MAINTAINER "rob.young@canarie.ca"

# When creating the container, the following
# RUN commands will be run in order to build it up
RUN yum update -y
RUN yum -y install tar unzip curl which

RUN curl -o /tmp/elasticsearch-1.6.0.tar.gz -SL https://download.elastic.co/elasticsearch/elasticsearch/elasticsearch-1.6.0.tar.gz

# Download Oracle JDK and install
RUN curl -o /tmp/jdk-7u79-linux-x64.tar.gz -k -SL -H "Cookie: oraclelicense=accept-securebackup-cookie"   http://download.oracle.com/otn-pub/java/jdk/7u79-b15/jdk-7u79-linux-x64.tar.gz

# Install compressed packages
RUN tar -zxvf /tmp/jdk-7u79-linux-x64.tar.gz -C /
RUN mkdir /usr/local/lib/elastic/ && tar -zxvf /tmp/elasticsearch-1.6.0.tar.gz -C /usr/local/lib/elastic/

ENV JAVA_HOME /jdk1.7.0_79
ENV PATH ${PATH}:/jdk1.7.0_79/bin

# Install Elasticsearch head plugin
RUN /usr/local/lib/elastic/elasticsearch-1.6.0/bin/plugin -install mobz/elasticsearch-head

# Add the contents of the elastic directory to the
# container
ADD elastic/ /usr/local/lib/elastic

EXPOSE 80

# On running the container, run the following command
CMD /usr/local/lib/elastic/runElasticSearch.sh
