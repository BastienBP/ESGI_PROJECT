FROM python:2
RUN mkdir /data
WORKDIR /data
RUN apt-get update
RUN apt-get install python-software-properties -y
RUN pip install kafka
RUN pip install tweepy

ENTRYPOINT [ "python", "./producer/producer.py" ]
