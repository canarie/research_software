# Dockerized elasticsearch demo

## Overview
This Docker image contains a demo version of Elasticsearch mentioned in the forthcoming
CANARIE white paper "Getting started with Elasticsearch".  This container is intended to demonstrate how Elasticsearch can be configured for a development/testing environment using in-memory storage.  This container includes the elasticsearch head plugin ( https://mobz.github.io/elasticsearch-head/ ) for ease of debugging.  

For a more complex elasticsearch container, see https://hub.docker.com/_/elasticsearch/

## Links
 * [GitHub](https://github.com/canarie/research_software/tree/master/docker/elasticsearch)
 * [Docker Hub](https://hub.docker.com/r/canarie/elasticsearchdemo/)

## Usage
To run this container, run the following two docker commands.

	docker pull canarie/elasticsearchdemo:latest

	docker run --name canarieelasticdemo -d -p 8000:80 canarie/elasticsearchdemo

Once the container is running, the elasticsearch head plugin can be viewed by browsing to

	http://<docker host IP>:8000/_plugin/head/

## Licence

See https://github.com/canarie/research_software/tree/master/docker/elasticsearch/licence.md

## Feedback

Questions, issues and suggestions can be sent to software@canarie.ca.
