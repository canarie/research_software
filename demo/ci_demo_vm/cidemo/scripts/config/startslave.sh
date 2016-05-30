#!/bin/bash

java -jar /home/vagrant/slave.jar -jnlpUrl http://localhost:8080/computer/Host_Node/slave-agent.jnlp > /dev/null &

PID=$!
echo "${PID}" > /home/vagrant/host_node/jenkins.pid
echo "Started"
