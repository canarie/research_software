# cidemo Containers

## appserver
httpd based docker image that serves three static files: a.html, b.html and index.html.  This container is used to provide a mock application server that would be the application under test in a real testing setup.

## brokenappserver
Clone of the appserver image where b.html is unavailable and a.html returns bad data.

## test1
Containerized hello world, running under python 2.7.

## test2
Containerized hello world, running under python 3.5.1.

## test3selenium
Tests a linked application server using a linked Selenium Hub.  Contains python based selenium tests.  This container requires two named linked containers for correct operation: web and seleniumhub.
