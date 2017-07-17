FROM python:2
RUN apt-get update
RUN apt-get install python-software-properties -y
RUN apt-get install g++-4.8 -y
RUN apt-get install python-dev libsasl2-dev -y gcc -y
RUN apt-get install sasl2-bin -y libsasl2-modules-gssapi-mit -y
RUN pip install pyhs2
RUN pip install flask
RUN pip install pandas

WORKDIR /src
COPY app.py /src/app.py
COPY cluster.cfg /src/cluster.cfg
COPY templates /src/templates
#CMD ["bash"]
CMD [ "python","app.py"]
