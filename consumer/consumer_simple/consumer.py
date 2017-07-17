#! /usr/bin/env python
# -*- coding: utf-8 -*-

import time

import logging
import logging.config
from logging.handlers import RotatingFileHandler
from pykafka.common import OffsetType
from kafka import KafkaConsumer
from kafka import TopicPartition
import pyhs2
import json

with open("params.json") as f:
    data = json.load(f)

server_port = data['server_port']
table_hive = data['table_hive']
lenght_bloc = data['lenght_bloc']
log_file = data['log_file']['consumer']
topic = data['topic']
host_hive = data['host_hive']
user_hive = data['user_hive']
password_hive = data['password_hive']
database_hive = data['database_hive']
broker1 = data['cluster']['broker1']
broker2 = data['cluster']['broker2']
broker3 = data['cluster']['broker3']

####### LOGGING CONFIG #######
logging.basicConfig()
logger = logging.getLogger('consumer')
logger.setLevel(logging.INFO)#ERROR
logger.info("initialize logger")
logger.propagate = False
fh = RotatingFileHandler(log_file, maxBytes = 2*1024*1024, backupCount = 5)# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)
logger.info("initialize logger finished")
############################

topic = TopicPartition(topic,0)


def get_consumer_kafkaConsumer():
        consumer = KafkaConsumer(group_id='my-group1',bootstrap_servers=[broker1+':'+server_port,broker2+':'+server_port,broker3+':'+server_port])
        consumer.assign([topic])
        position = consumer.position(topic)
        consumer.seek_to_end(topic)
        return consumer

def get_tweet(consumer):
    try:
        messages = []
        for message in consumer:
            if message is not None:
	        print message.value
                current_offset = message.offset
                logger.info('retrieving message n_° %s' % current_offset)
                with pyhs2.connect(host=host_hive,port=10000,authMechanism="PLAIN",user=user_hive,password=password_hive,database=database_hive) as conn:
                    logger.info("Connected to hive")
                    with conn.cursor() as cur:
                        #Show databases
                        current_database = cur.getDatabases()
                        logger.info("Current database:"+str(current_database))
                        #while len(messages)<31:
                        messages.append((message.offset, message.value.replace('"','\22').encode('ascii', 'ignore'), time.strftime("%Y%m")))
                        print len(messages)
                        if len(messages)==lenght_bloc:
                            print messages
                            cur.execute("create table if not exists "+table_hive+"(ID varchar(255), value string, time string)")
                            messages = ','.join(str(messages[i]) for i in range(len(messages)))
                            stmt = "INSERT INTO "+table_hive+" VALUES " + messages
                            print stmt
                            cur.execute(stmt)
                            messages = []
                    		#cur.execute("create table if not exists twitter_grippe(ID varchar(255), tweet string, date_month string)")
                    		#cur.execute('INSERT INTO table twitter_grippe values ('{}','{}','{}')".format(message.offset, message.value, time.strftime("%Y%m")))
            elif not message:
                print 'No message'
            else:
                print 'Something else happened..'
    except KeyboardInterrupt as e:
            pass
    return message.offset, message.value, time.strftime("%Y%m")



if __name__ == '__main__':
        consumer = get_consumer_kafkaConsumer()
        id, message, date_month = get_tweet(consumer)
        print id, message, date_month
