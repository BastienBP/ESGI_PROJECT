FROM python:2
RUN mkdir /data
WORkDIR /data
RUN apt-get update
RUN apt-get install python-software-properties -y
RUN apt-get install g++-4.8 -y
RUN apt-get install python-dev libsasl2-dev -y
RUN pip install pykafka
RUN pip install kafka
RUN pip install pyhs2


CMD [ "python", "./consumer/consumer_from_position.py" ]

