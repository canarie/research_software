FROM python:3.5.1

RUN pip install selenium
RUN pip install nose
RUN pip install requests

# Install the dockerize command
RUN wget https://github.com/jwilder/dockerize/releases/download/v0.2.0/dockerize-linux-amd64-v0.2.0.tar.gz && tar -C /usr/local/bin -zxvf dockerize-linux-amd64-v0.2.0.tar.gz

# COPY all integration test files to the container directory /tests
COPY scripts/ /scripts
RUN chmod u+x /scripts/run.sh

CMD /scripts/run.sh
