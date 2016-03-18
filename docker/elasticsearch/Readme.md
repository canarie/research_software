# Elastic Search Demo
## Overview
This Docker image contains a demo version of Elasticsearch mentioned in the
CANARIE white paper "Getting started with Elasticsearch".  This container is intended to demonstrate how Elasticsearch can be configured for a development/testing environment using in-memory storage.  This container includes the elasticsearch head plugin for ease of debugging.  

For a more complete and complex elasticsearch container, see https://hub.docker.com/_/elasticsearch/

## Usage
To run this container, run the following two docker commands.

	docker pull canarie/elasticsearchdemo:latest

	docker run --name canarieelasticdemo -d -p 8000:80 canarie/elasticsearchdemo

Once the container is running, the elasticsearch head plugin can be viewed by browsing to

	http://<docker host IP>:8000/_plugin/head/
