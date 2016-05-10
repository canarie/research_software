# cidemo - Continuous Integration Demonstration Virtual Machine
This directory is the base root for all files related to the cidemo VM.  It also contains a number of docker images for use in this VM.  It's intended purpose is to demonstrate an end to end docker based selenium tests.  

## Key Features
When the VM is provisioned with Vagrant (i.e. vagrant up cidemo), it has the following key features:

 * running docker host containing the following containers:
 	* docker registry running on port 5000.
	* Jenknis CI.
    * Selenium hub with one FireFox and one Chrome node attached.
	* three stub python based tests.
	* two stub application servers.
 * the docker image in each directory under the directory containers will be built and pushed to the local docker repository running on port 5000.
 * a docker slave node running on the host VM environment.
