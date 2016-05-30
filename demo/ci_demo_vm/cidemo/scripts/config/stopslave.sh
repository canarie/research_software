#!/bin/bash

PID=`cat /home/vagrant/host_node/jenkins.pid`
kill ${PID}
echo "Ended"
