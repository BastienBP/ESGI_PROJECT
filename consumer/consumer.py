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
topic = data['topic']
host_hive = data['host_hive']
user_hive = data['user_hive']
password_hive = data['password_hive']
database_hive = data['database_hive']
broker1 = data['cluster']['broker1']
broker2 = data['cluster']['broker2']
broker3 = data['cluster']['broker3']

topic = TopicPartition(topic,0)


def get_consumer_kafkaConsumer():
        consumer = KafkaConsumer(group_id='my-group1',bootstrap_servers=[broker1,broker2,broker3])
        consumer.assign([topic])
        position = consumer.position(topic)
        consumer.seek_to_end(topic)
        return consumer

def get_tweet(consumer):
    try:
        messages = []
        for message in consumer:
            if message is not None:
                    #print message.offset, message.value.replace('"','\"'), time.strftime("%Y%m")

            	with pyhs2.connect(host=host_hive,port=10000,authMechanism="PLAIN",user=user_hive,password=password_hive,database=database_hive) as conn:
                    print "Connected to hive"
                    with conn.cursor() as cur:
                        #Show databases
                        print cur.getDatabases()
                        print "retrieving messages"
                        #while len(messages)<31:
                        messages.append((message.offset, message.value.replace('"','\22').encode('ascii', 'ignore'), time.strftime("%Y%m")))
                        if len(messages)==30:
                            #print messages
                            cur.execute("create table if not exists kafka(ID varchar(255), value string, time string)")
                            messages = ','.join(str(messages[i]) for i in range(len(messages)))
                            stmt = "INSERT INTO kafka VALUES " + messages
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
