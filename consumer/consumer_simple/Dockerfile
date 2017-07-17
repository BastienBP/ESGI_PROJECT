FROM python:2
RUN apt-get update
RUN apt-get install python-software-properties -y
RUN apt-get install g++-4.8 -y
RUN apt-get install python-dev libsasl2-dev -y gcc -y
RUN apt-get install sasl2-bin -y libsasl2-modules-gssapi-mit -y
RUN pip install pykafka
RUN pip install kafka
RUN pip install pyhs2

WORKDIR /src
COPY consumer.py /src/consumer.py
COPY params.json /src/params.json
COPY logger_kafka/ /src/logger_kafka/
#COPY offset.cfg /src/offset.cfg
#CMD ["bash"]
CMD [ "python","consumer.py"]

