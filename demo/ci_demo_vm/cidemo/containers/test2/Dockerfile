FROM python:3.5.1

RUN pip install nose

COPY scripts/ /scripts
RUN chmod u+x /scripts/run.sh

CMD /scripts/run.sh
