NEP-RPI Reference Service and Platform Application Note
=======================================================

## Introduction

This application note describes the CANARIE Research Software Reference application. It demonstrates a simple implementation of the NEP-RPI API as described in the documents entitled “Research Service Support for the CANARIE Registry and Monitoring System”, revision 6 and “Research Platform Support for the CANARIE Registry and Monitoring System”, revision 2. The aim of this document is explain the design of the application, how to use it and some notes on deploying it in a production environment.

The service is written using the following technologies and frameworks:

- [Python  - programming language](https://www.python.org/)
- [django  - web development framework](https://www.djangoproject.com/) 
- [django-rest-framework  – REST frame work for django](http://www.django-rest-framework.org/)
- [celery  - task queue](http://www.celeryproject.org/)
- [requests  – Python HTTP library](http://www.python-requests.org/)


The reference application functionality has deliberately been kept very simple. It consists of a service that count the number of times it is invoked and a platform that can regularly invoke the service. Both the platform and service implement the appropriate CANARIE Research Software APIs.

## Application Design

The service follows the layout of a standard django project with the following structure:

	reference
		- integration
		- project	
			canarie_platform
			canarie_service
			project
			util
			logs

The code is contained within the reference/project directory and subdirectories. The main django management script is contained at this root level.

	manage.py – Allows starting of the development server, running unit tests and accessing the Python iterative console with django support configured.

The subdirectory reference/project/project directory contains all of the site wide configuration and deployment details. The main files here are:

	settings.py and settings-prod.py – The configuration settings for the default development and production deployment respectively.
	urls.py – Which contains the basic site URL routing
	wsgi.py and wsgi-prod.py – Contains the configuration to allow apache’s mod_wsgi module to server the site. The configuration for the django development
	server is in wsgi.py and the configuration for apache in a production deployment is in wsgi-prod.py

The main site code for the application is contained in the reference/project/canarie_service and  reference/project/canarie_platform directories. The main files used for each of these are:

	defaults.py – Contains some default settings for the component.
	models.py – Contains the database model for the application. This is used by django to configure the database schema and by the application to connect with the database.
	serializers.py – Contains classes to serialize the Python data representations into the JSON format required by the API.
	tests.py – Unit tests to test the functionality of the application. In this project all of the unit tests are contained in this one file.
	views.py – This is the main application code for the applications, handles rendering of the API responses.
	urls.py – Configures the URL routing to view based on regular expression rules.
	templates/ - This subdirectory contains the templates for the various HTML pages rendered by the view.

The reference/project/canarie_platform directory also contains some additional files.
	
	tasks.py – The celery task that is used to run the polling.
	utility.py – Some utility functions used in by the platform. 

The reference/project/util directory contains some shared utilities for both the service and platform.

At a high level the basic flow of a request through this system is as follows. The requested URL is compared to the regular expressions in reference/project/project/urls.py. It is then passed to the urls.py in the appropriate application where is compared to the URLs configured there. If a match is made, the URL is passed to the appropriate handler in the views.py file.

In both cases the view script, view.py, contains all of the actual application processing. This file is divided into three sections. The first section contains all of the methods required to handle the CANARIE RPI API, the two most notable methods being ‘info’ and ‘stats’ which are annotated with and api_view from the django-rest-framework API to help with processing REST calls. These methods check to see what ‘Accept’ header has been set in the request. If it is ‘application/json’ then a JSON representation of the data is returned; otherwise an HTML representation is rendered from the appropriate template.  The rest of the API methods either redirect to an appropriate URL or return a rendered template directly.

The second section of file view.py contains methods to run the sample applications that the API is reporting on. The sample applications have deliberately been kept a very simple in order to just outline the use of the API. 

For the service the main app method renders a page template with the current statistic data and contains a form for incrementing the count and resetting it. The ‘usage’ method is called from the form submit, then depending on the form fields that have been set the it calls method to either increment the counter or reset it and store the last update time. There are also two methods, ‘add’ and ‘reset’ to expose this functionality programmatically. The final method in this section allows the service ‘info’ to be updated via a REST PUT.

The platform renders a simple control for that allows starts and stops a random polling to the service. The page displays the number of interactions with the platform, that last time the statistics were reset, whether it is currently polling the service or not and the currently configured min and max second values for each subsequent poll.

The third section contains utility methods to support the API and application.

## How to use the service

This section will explain how to use the service application.

#### Main application

##### Browse to:

	<server-base-url>/reference/service/app 

This page will display the current usage stats. Clicking on the ‘Count’ button will increment the usage count by one. Clicking on ‘Reset’ will reset the counter to ‘0’ and set the last reset time to the current server time in UTC. In either case the page will be re-rendered and the current values displayed. 
The following REST calls are also available to interact with the application. When calling the REST method the ‘Accept’ HTTP header needs to be set to ‘application/json’ in order to make the request.

##### Add

	PUT <server-base_url>/reference/service/add – to increment the usage counter programmatically

This will return a JSON object with the new values, in the form detailed in the CANARIE Research Middle ware API for ‘stats’, i.e.

	{	
		“invocations” : “<invocation-count>”,
		“lastReset” :	 “<last-reset-time>”
	} 

##### Reset

	PUT  <server-base_url>/reference/service/reset – to reset the usage counter and last reset time programmatically.

This will return the same JSON as for ‘add’ which contains a ‘invocations’ value of ‘0’ and the new ‘lastReset’ time in ISO8601 as detailed in the in the CANARIE Research Middleware API document.

##### SetInfo

	PUT <server-base_url>/reference/service/setinfo

This expects a JSON payload in the form of the ‘info’ object detailed in the CANARIE Research Middle ware API document. i.e.

The info settings for the service will be updated with the new values and it will return a JSON object containing these new settings in the same format. 

Release time should be in the format ‘%Y-%m-%dT%H:%M:%SZ’. 

#### General usage

The application will also respond to the URLs detailed in “Research Service Support for the CANARIE Registry and Monitoring System” with the correct data.

## How to use the platform

This section explains how to use the platform.

#### Main application

##### Browse to:

	<server-base-url>/reference/platform/app 

The will display a simple page that allows you to see the current stats about the platform and along with the current service polling state. There are buttons to start and stop the polling as well as a button to reset the current usage count. Both starting and stopping the service will result in a usage increase.

##### Start

	PUT <server-base-url>/reference/platform/start

This will start polling to the reference service.  The response will be a JSON in the following format:
	
	{“running”: true}

##### Stop

	PUT <server-base-url>/reference/platform/stop

This will stop polling to the reference service. The response will be a JSON in the following format:

	{“running”: false}

##### Reset

	PUT <server-base-url>/reference/platform/reset

This will return a JSON object with the new values, in the form detailed in the CANARIE Research Middle ware API for ‘stats’, i.e.

	{	
		“interactions” : “0”,
		“lastReset” :	 “<last-reset-time>”
	}

##### SetInfo

	PUT <server-base_url>/reference/service/setinfo

This expects a JSON payload in the form of the ‘info’ object detailed in the CANARIE Research Middle ware API document. i.e.

	{		
		“name” : “<new-name>”,
		“synopsis” :	 “<new-synopsis>”,
		“version” : “<new-version>”,
		“institution” : “<new-institution>”,
		“releaseTime” : “<new-release-time>”,
		“researchSubject” : ”<new-research-subject>”,
		“supportEmail” : “<new-support-email>”,
		“tags” : [“<new-tag-1>”, “<new-tag-2>” …]
	} 

The info settings for the service will be updated with the new values and it will return a JSON object containing these new settings in the same format.

Release time should be in the format ‘%Y-%m-%dT%H:%M:%SZ’. 

## Admin console

Many of the parameters and settings can also be modified using the django administration console. This can be accessed at:

	 <server-base_url>/admin

The admin credentials are those supplied when the django database is created. More user credentials can be created if needed. This admin console allows administration of both service and platform data. The database is populated with default data the first time that data is accessed. So, for example, browsing to the platform/info page may be required after installation to populate the default info data. 

## Deployment

There are two deployment options when using django, development where django’s own built in webserver serves the pages and production where a full webserver, such as Apache is used.

#### General configuration

To install the required libraries a requirements.txt file is provided in the reference project. To install all of the libraries the following command can be run:

	pip install –r requirements.txt

In both the development and production cases the database needs configuring before the first use. To do this change into the /reference/project directory and execute the following commands:
	
	./manage.py makemigrations
	./manage.py migrate

An admin user should be created when prompted to be able to access the web based admin console.

## Development

The development version is a quick way of seeing the service in action and for development and testing. It can be run in this mode using the following command:

	python manage.py runserver 

This will launch the webserver running on port 8000 and allow it to be accessed at this base URL:

	http://127.0.0.1:8000/

The celery server will also need to be running and can be started using the following command:

	celery -q -A project worker --statedb=./celery.worker.state

## Production

When running in a production environment some changes to the way the application is run need to be made.

#### Celery 

In production celery should be run as a daemon process, so if you use this technology in your own projects please see the following documentation for more details: 

	http://docs.celeryproject.org/en/latest/userguide/daemonizing.html

#### Django

In order to use a django application for anything more than development or testing then it needs to be configured to work with a webserver using the wsgi interface. The instructions below detail the steps that were necessary to run the application with the apache web server on a Centos 7 virtual machine running on CANARIE’s DAIR cloud. The steps start from the initial creation of the virtual machine and may not all be necessary depending on the deployment environment.

On a different system the specifics may change but the principle steps should remain similar.

#### Create DAIR instance 

This section deals with creating the DAIR instance and installing the correct dependencies. Initially create the DAIR instance using the following settings.

	OS: CentOS 7
	HD Volume on /dev/vdc
	Log in with an SSH session as per instructions in DAIR user docs

##### Create reference user

	sudo useradd reference
	sudo passwd reference

##### Add to sudoers

	sudo visudo

Add line for the reference user

	reference All=(ALL) ALL

##### Format and mount the volume as per the DAIR docs and change ownership to reference

##### Add paths to PATH environment variable
	sudo vi ~/.bash_profile

Add these paths

	/usr/local/bin
	/home/reference/.local/bin/

##### Turn off SE linux

	sudo vi /etc/selinux/config

Change SELINUX=enforcing to SELINUX=permissive and save the file.

###### Install apache

	sudo yum install -y httpd mod_ssl

Install the IUS repository:

	sudo curl 'https://setup.ius.io/' -o setup-ius.sh
	sudo sh setup-ius.sh

Replace the version of Apache from the CentOS repository with the IUS version:

	sudo yum -y install yum-plugin-replace
	sudo yum -y replace httpd --replace-with httpd24u

Set apache to start on boot

	sudo systemctl enable httpd


###### Install Python 3.6

	sudo yum install –y https://cenots7.iuscommunity.org/ius-release.rpm
	sudo yum update
	sudo yum install –y python36u python36u-libs python36u-develp python36u-pip

###### Install pip, virtualenv

	sudo yum –y install python-pip
	sudo pip install --upgrade pip
	sudo pip install virtualenv

###### Install mod_wsgi for Python3.6

	sudo yum install python36u-mod_wsgi.x86_64

Add mod_wsgi to apache 

	sudo vim /etc/httpd/conf/httpd.conf

Add to load module section

	LoadModule wsgi_module modules/mod_wsgi.so

Restart apache 
	
	sudo service httpd restart

###### Configure iptables to allow http

	sudo firewall-cmd --zone=public --add-port=80/tcp --permanent
	sudo firewall-cmd --zone=public --add-port=443/tcp --permanent
	sudo firewall-cmd --zone=public --add-service=https --permanent
	sudo firewall-cmd --zone=public --add-service=http –permanent
	sudo firewall-cmd --reload

At this point if we browse to the server using a web browser we should get a standard apache test page

	http://<vm-ipaddress>

##### Add django service code

Make web dir
	
	cd /media/volume1/
	mkdir -p srv/www

From external machine push research_software/reference

	tar cvfz ref_service.tar.gz research_software/reference
	scp -i ~/.ssh/dair_reference.pem ref_service.tar.gz centos@<vm-ipaddress>:

Unpack tar (Back on server)

	sudo cp /home/centos/ref_service.tar.gz srv/www
	cd srv/www
	sudo chown reference:reference ref_service.tar.gz
	tar -xvf ref_service.tar.gz

Change ownership of dirs so apache can access
	
	cd /media/volume1/srv/www
	sudo chown -R reference:apache .
	sudo chmod 775 reference/project

##### Make virtual environment

	cd /media/volume1
	mkdir venv
	cd venv
	virtualenv -p /usr/bin/python3.6 ENV
	. ENV/bin/activate

##### Install python packages (ENSURE virtualenv still sourced, prompt starts with (ENV))

	cd /media/volume1/srv/www/research_software/reference
	pip install –r requirements.txt

##### Configure an apache Virtual Host to serve the django pages

	sudo vi /etc/httpd/conf.d/reference.conf

	# Forward all port 80 (http) requests to https
	<VirtualHost *:80>
	   RewriteEngine On
	   RewriteCond %{HTTPS} off
	   RewriteRule (.*) https://%{HTTP_HOST}%{REQUEST_URI}
	</VirtualHost>
	
	# Serve static files
	Alias /static/ /media/volume1/srv/www/research_software/reference/project/static/
	
	<Directory /media/volume1/srv/www/research_software/reference/project/static/ >
	        Require all granted
	</Directory>
	
	# point Django to our custom settings file location
	SetEnv DJANGO_SETTINGS_MODULE project.settings
	
	# Django WSGI module
	LoadModule wsgi_module /usr/lib64/httpd/modules/mod_wsgi.so
	
	# set up WSGI to handle all addresses (at least those not excepted in Location directives above)
	WSGIScriptAlias / /media/volume1/srv/www/research_software/reference/project/project/wsgi-prod.py
	WSGIPythonHome /media/volume1/venv/ENV
	WSGIPythonPath /media/volume1/srv/www/research_software/reference/project
	WSGIDaemonProcess REFERENCE python-home=/media/volume1/venv/ENV python-path=/media/volume1/srv/www/research_software/reference/project
	WSGIProcessGroup REFERENCE 

	# ensure sufficient permissions to access the WSGI processor file
	<Directory /media/volume1/srv/www/research_software/reference/project/project>
	    <Files wsgi-prod.py>
	        Require all granted
	    </Files>
	</Directory>

##### Configure WSGISocketPrefix dir for wsgi

	cd /media/volume1/
	mkdir -p run/wsgi
	sudo chown -R apache:apache run

Restart apache
	
	sudo service httpd restart

Browse to application
	
	https://<vm-ipaddress>/reference/service/app

 