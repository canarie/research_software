#!/bin/bash

for D in `find /vagrant/cidemo/containers -type d -maxdepth 1 -mindepth 1`
do
    # Do whatever you need with D

	echo "Entering directory ${D}"
	CONTAINER_NAME=canarie/`basename ${D}`
	echo "Container name ${CONTAINER_NAME}"

	docker build -t "${CONTAINER_NAME}" $D

	docker tag "${CONTAINER_NAME}" localhost:5000/"${CONTAINER_NAME}"

	docker push localhost:5000/"${CONTAINER_NAME}"
done
