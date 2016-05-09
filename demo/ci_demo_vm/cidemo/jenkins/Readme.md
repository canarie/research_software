# Jenkins root

This directory contains a base jenkins configuration that is used at VM start up to provide a base configuration for the Jenkins Continuous Integration server.  This configuration includes:
 * a number of tests that demonstrate various concepts
 * a slave node named "Host_Node" that is used to execute jobs from the native VM host environment (i.e. outside the docker container environment)

## Authentication note
No authentication is set up as part of this demonstration!
