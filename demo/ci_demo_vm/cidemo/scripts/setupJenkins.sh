#!/bin/bash
#
#  Copyright 2014 - CANARIE Inc. All rights reserved
#
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


cp -rv /vagrant/cidemo/jenkins /home/vagrant/jenkins
chown -R vagrant:vagrant /home/vagrant/jenkins

echo "Install jenkins container"
docker run -d -p 8080:8080 -p 50000:50000 --name jenkins --restart always -v /home/vagrant/jenkins:/var/jenkins_home jenkins || echo "Could not create Jenkins CI!"

sudo yum -y install java-1.8.0-openjdk wget

# TODO install java jar correctly
sleep 10
wget -O /home/vagrant/slave.jar http://localhost:8080/jnlpJars/slave.jar
java -jar /home/vagrant/slave.jar -jnlpUrl http://localhost:8080/computer/Host_Node/slave-agent.jnlp > /dev/null &

# could create a job here https://gist.github.com/stuart-warren/7786892
