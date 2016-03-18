#!/bin/bash

# Copyright 2016 - CANARIE Inc. All rights reserved
#
# Synopsis: Integration helper script used to drive elastic search server.
# This is not used by the container but left in the repository to provide another
# option for managing elasticsearch instances outside of a container.
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

export BUILD_INST_DIR=/media/volume1/jenkins/build
export JENKINS_HOME=$BUILD_INST_DIR/jenkins_home
export CANARIE_DIR=`pwd`

RUNNING_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
DESC="ElasticSearch server"
NAME="elasticsearch_helper.sh"
ELASTIC_PATH=${RUNNING_DIR}/elasticsearch-1.6.0/bin
PID_FILE=
NODE_NAME=
CLUSTER_NAME=
CLUSTER_HTTP_PORT=
CLUSTER_TRANSPORT_PORT=
SERVER_TYPE=
RPI_PORT=${RPI_PORT:-8080}

d_start() {
	# start domain if not up
	echo "Starting ElasticSearch"
	echo "   Node name: ${NODE_NAME}"
	echo "   Cluster name: ${CLUSTER_NAME}"
	echo "   Http port: ${CLUSTER_HTTP_PORT}"
	echo "   Transport port: ${CLUSTER_TRANSPORT_PORT}"
	echo "   PID file: ${PID_FILE}"

	if [ -e "${PID_FILE}" ]
	then
		echo "PID file already exists, attempting to kill existing instance"
		read pid <${PID_FILE}

		kill ${pid}

		sleep 1

		if [ -e "${PID_FILE}" ]
		then
			echo "WARNING - PID file still exists!"
		fi
	fi
	${ELASTIC_PATH}/elasticsearch  \ #-d
		-p ${PID_FILE} --index.store.type=memory \
		--node.name=${NODE_NAME} --cluster.name=${CLUSTER_NAME} \
		--http.port=${CLUSTER_HTTP_PORT} \
		--transport.tcp.port=${CLUSTER_TRANSPORT_PORT}

	elast_ret_code=$?

	if [ $elast_ret_code != 0 ]; then
		printf "Error starting ElasticSearch!"

		exit $elast_ret_code
	fi

	echo "Started ElasticSearch"

	echo "Attempting to update index via glassfish"
	curl -X PUT "http://localhost:${RPI_PORT}/researchmiddleware/rs/private/researchresource/elastic/"

	curl_ret_code=$?

	if [ $curl_ret_code != 0 ]; then
		printf "Could not update index via glassfish"
	else
		printf "Updated index successfully!"
	fi

	printf "Curl ret code is ${curl_ret_code}"
}

d_stop() {
	if [ -e "${PID_FILE}" ]
	then
		echo "Shutting down Elasticsearch"
		curl -X POST -f http://localhost:${CLUSTER_HTTP_PORT}/_cluster/nodes/_local/_shutdown
		echo
		sleep 2
		if [ -e "${PID_FILE}" ]
		then
			echo "Elasticsearch seems to still be running, attempting to kill via pid."
			read pid <${PID_FILE}

			kill ${pid}
			echo "Found PID file ${PID_FILE}, sent kill signal."
			exit $?
		else
			echo "Elasticsearch has been shut down successfully!"
			exit 0
		fi
	else
		echo "Could not find pid file ${PID_FILE}"
		exit 1
	fi
}

d_status() {
	if [ -e "${PID_FILE}" ]
	then
		echo "Server PID file ${PID_FILE} exists"
	else
		echo "Server PID file ${PID_FILE} does not exist"
	fi

	echo "Attempting to contact server on HTTP port ${CLUSTER_HTTP_PORT}"
	curl -G http://localhost:${CLUSTER_HTTP_PORT}/?pretty

	if [ $? -ne 0 ]; then
	    echo "Could not contact server"
	else
		echo "Server is responding to requests"
	fi
    exit 0
}

d_usage() {
	echo "usage: $NAME {start|stop|status} {dev|integration|production}"
	echo "This script is used for managing elastic search.  It manages three server instances, dev, integration, and production.  Both servers are set up to use in memory data storage."
	exit 1
}

echo "Running directory is ${RUNNING_DIR}"

case $2 in
	dev)
	PID_FILE=${RUNNING_DIR}/elastic-dev.pid
	NODE_NAME=dev
	CLUSTER_NAME=rsdev
	CLUSTER_HTTP_PORT=9201
	CLUSTER_TRANSPORT_PORT=9301
	SERVER_TYPE=DEV
	;;
	integration)
	PID_FILE=${RUNNING_DIR}/elastic-integration.pid
	NODE_NAME=integration
	CLUSTER_NAME=rsintegration
	CLUSTER_HTTP_PORT=9202
	CLUSTER_TRANSPORT_PORT=9302
	SERVER_TYPE=INTEGRATION
	;;
	production)
	PID_FILE=${RUNNING_DIR}/elastic-prod.pid
	NODE_NAME=prod
	CLUSTER_NAME=rsprod
	CLUSTER_HTTP_PORT=9203
	CLUSTER_TRANSPORT_PORT=9303
	SERVER_TYPE=PRODUCTION
	;;
	*)
	echo "ERROR - unknown server type $2!"
	d_usage
	exit 1
	;;
esac

case $1 in
	start)
	echo "Starting $DESC (${SERVER_TYPE}): $NAME"
	d_start
	echo "."
	;;
	stop)
	echo "Stopping $DESC (${SERVER_TYPE}): $NAME"
	d_stop
	echo "."
	;;
	status)
	d_status
	;;
	*)
	d_usage
	;;
esac

exit 0
