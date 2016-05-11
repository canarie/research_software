FROM python:2.7

RUN pip install nose

COPY scripts/ /scripts
RUN chmod u+x /scripts/run.sh

CMD /scripts/run.sh
