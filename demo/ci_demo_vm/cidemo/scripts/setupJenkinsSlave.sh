#!/bin/bash

echo "Setting up jenkins slave node"
wget -O /home/vagrant/slave.jar http://localhost:8080/jnlpJars/slave.jar
java -jar /home/vagrant/slave.jar -jnlpUrl http://localhost:8080/computer/Host_Node/slave-agent.jnlp > /dev/null &
