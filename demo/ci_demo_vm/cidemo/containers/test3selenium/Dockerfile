FROM python:3.5.1

RUN pip install selenium
RUN pip install nose
RUN pip install requests

# COPY all integration test files to the container directory /tests
COPY scripts/ /scripts
RUN chmod u+x /scripts/run.sh

CMD /scripts/run.sh
