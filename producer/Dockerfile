FROM python:2
RUN mkdir /data
WORKDIR /data
RUN apt-get update
RUN apt-get install python-software-properties -y
RUN pip install kafka
RUN pip install tweepy
WORKDIR /src
COPY producer.py /src/producer.py
COPY params.json /src/params.json
COPY logger_kafka/ /src/logger_kafka/
#COPY offset.cfg /src/offset.cfg
COPY config.json /src/config.json

ENTRYPOINT [ "python", "producer.py" ]

