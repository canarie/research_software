# Provisioning Scripts

This directory contains all of the scripts used in provisioning the Vagrant based
cidemo VM.  Bash scripting was chosen as the provisioning language for ease of reading.

## provision.sh
Main provisioning script which bootstraps the process.

## setupJenkins.sh
Copies the base Jenkins configuration to a local directory and starts a docker container running Jenkins CI.

## setupSelenium.sh
With prebuilt docker images, creates a Selenium Hub server and two Selenium nodes (one FireFox, one Chrome).

## setupRegistry.sh
Sets up a local docker registry.

## buildContainers.sh
Builds each container image under the directory cidemo/containers and pushes them to the local registry.

## setupJenkinsSlave.sh
Creates a Jenkins slave node on the host VM.
