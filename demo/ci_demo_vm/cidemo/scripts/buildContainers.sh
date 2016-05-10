#!/bin/bash
#
#  Copyright 2016 - CANARIE Inc. All rights reserved
#
#  Synopsis: Builds all containers directly under the directory
#  /vagrant/cidemo/containers
#  All containers are build, tagged, and pushed to the local docker repository.
#
#  -------------------------------------------------------------------------------
#
#  Blob Hash: $Id$
#
#  -------------------------------------------------------------------------------
#
#  Redistribution and use in source and binary forms, with or without modification,
#  are permitted provided that the following conditions are met:
#
#  1. Redistributions of source code must retain the above copyright notice,
#     this list of conditions and the following disclaimer.
#
#  2. Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions and the following disclaimer in the documentation
#     and/or other materials provided with the distribution.
#
#  3. The name of the author may not be used to endorse or promote products
#     derived from this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY CANARIE Inc. "AS IS" AND ANY EXPRESS OR IMPLIED
#  WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
#  MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
#  EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#  EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
#  OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
#  INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
#  CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
#  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
#  POSSIBILITY OF SUCH DAMAGE.

LOCAL_REGISTRY="localhost:5000"

for D in `find /vagrant/cidemo/containers -type d -maxdepth 1 -mindepth 1`
do
	echo "Entering directory ${D}"
	CONTAINER_NAME=canarie/`basename ${D}`

	echo "Building container ${CONTAINER_NAME}"
	docker build -t "${CONTAINER_NAME}" $D

	echo "Tagging ${CONTAINER_NAME}"
	docker tag "${CONTAINER_NAME}" ${LOCAL_REGISTRY}/"${CONTAINER_NAME}"

	echo "Pushing ${CONTAINER_NAME} to ${LOCAL_REGISTRY}"
	docker push ${LOCAL_REGISTRY}/"${CONTAINER_NAME}"
done
