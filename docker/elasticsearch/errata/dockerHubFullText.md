# Supported tags and respective Dockerfile links

* latest, v1 (repo-link to be added here)

Imagelayers link to be added here

The source files for these images can be found in the CANARIE elasticsearch repository.

# Dockerized elasticsearch demo
This Docker image contains a demo version of Elasticsearch mentioned in the
CANARIE white paper "Getting started with Elasticsearch".  This container is intended to demonstrate how Elasticsearch can be configured for a development/testing environment using in-memory storage.  This container includes the elasticsearch head plugin ( https://mobz.github.io/elasticsearch-head/ ) for ease of debugging.  

For a more complex elasticsearch container, see https://hub.docker.com/_/elasticsearch/

## Usage
To run this container, run the following two docker commands.

	docker pull canarie/elasticsearchdemo:latest

	docker run --name canarieelasticdemo -d -p 8000:80 canarie/elasticsearchdemo

Once the container is running, the elasticsearch head plugin can be viewed by browsing to

	http://<docker host IP>:8000/_plugin/head/

## Licence

See https://github.com/canarie/research_software/tree/master/docker/elasticsearch/licence.md
