#! /usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import logging.config
from logging.handlers import RotatingFileHandler
import inspect
import time
import ConfigParser
from pykafka.common import OffsetType
from kafka import KafkaConsumer
from kafka import TopicPartition
import pyhs2
import json

with open("../params/params.json") as f:
    data = json.load(f)
server_port = data['server_port']
lenght_bloc = data['lenght_bloc']
log_file = data['log_file']['consumer_from_position']
topic = data['topic']
host_hive = data['host_hive']
user_hive = data['user_hive']
password_hive = data['password_hive']
database_hive = data['database_hive']
table_hive = data['table_hive']
broker1 = data['cluster']['broker1']
broker2 = data['cluster']['broker2']
broker3 = data['cluster']['broker3']
topic = TopicPartition(topic,0)

####### LOGGING CONFIG #######
logging.basicConfig()
logger = logging.getLogger('consumer_from_position')
logger.setLevel(logging.INFO)#ERROR
logger.info("initialize logger")
logger.propagate = False
fh = RotatingFileHandler(log_file, maxBytes = 2*1024*1024, backupCount = 5)# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)
logger.info("initialize logger finished")
############################

def get_consumer_kafkaConsumer():
        consumer = KafkaConsumer(group_id='my-group1',bootstrap_servers=[broker1+':'+server_port,broker2+':'+server_port,broker3+':'+server_port])
        consumer.assign([topic])
        consumer.commit_async()
        consumer.poll()
        #position = consumer.position(topic)
        #consumer.seek_to_end(topic)
        return consumer

def get_consumer_kafkaConsumer_seek(cfg_offset):
        consumer = KafkaConsumer(group_id='my-group1',bootstrap_servers=[broker1+':'+server_port,broker2+':'+server_port,broker3+':'+server_port])
        consumer.assign([topic])
        position = consumer.position(topic)
        print cfg_offset
        consumer.seek(topic, int(cfg_offset)+1)
        return consumer

def config_parser():
    return ConfigParser.ConfigParser()

def config_parser_first_launch():
    cfg = config_parser()
    cfg.add_section("OFFSET")
    cfg.set("OFFSET","last_offset","0")
    cfg.set("OFFSET","is_reloaded?","false")
    cfg.write(open("offset.cfg",'w'))

def write_offset(offset):
    cfg = config_parser()
    cfg.add_section("OFFSET")
    cfg.set("OFFSET","last_offset",offset)
    cfg.set("OFFSET","is_reloaded?","true")
    cfg.write(open("offset.cfg",'w'))

def get_tweet(consumer):
    try:
        messages = []
        #########################################
        cfg = config_parser()
        cfg.read("offset.cfg")
        #cfg.add_section("OFFSET")
        cfg_offset = cfg.get("OFFSET","last_offset")
        cfg_statut = cfg.get("OFFSET","is_reloaded?")
        if cfg_statut == "false":
            position = consumer.position(topic)
            #first_offset = consumer.next()
            first_offset = consumer.get_message(block=True, timeout=0.1, get_partition_info=None)
            first_offset = first_offset.offset
            write_offset(first_offset)
            ############
            for message in consumer:
                if message is not None:
                    current_offset = message.offset
                    print current_offset
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
                                #print messages
                                cur.execute("create table if not exists "+table_hive+"(ID varchar(255), value string, time string)")
                                messages = ','.join(str(messages[i]) for i in range(len(messages)))
                                stmt = "INSERT INTO "+table_hive+" VALUES " + messages
                                print stmt
                                cur.execute(stmt)
                                messages = []
                                print "New offset! ->"+ str(current_offset)
                                logger.info("initialize first offset: "+str(current_offset))
                                write_offset(current_offset)

                        		#cur.execute("create table if not exists twitter_grippe(ID varchar(255), tweet string, date_month string)")
        else:

            for message in get_consumer_kafkaConsumer_seek(cfg_offset):
                if message is not None:
                    current_offset = message.offset
                    logger.info('retrieving message n_° %s' % current_offset)
                    print current_offset
                        #print message.offset, message.value.replace('"','\"'), time.strftime("%Y%m")
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
                                #print messages
                                cur.execute("create table if not exists "+table_hive+"(ID varchar(255), value string, time string)")
                                messages = ','.join(str(messages[i]) for i in range(len(messages)))
                                stmt = "INSERT INTO "+table_hive+" VALUES " + messages
                                print stmt
                                cur.execute(stmt)
                                messages = []
                                write_offset(current_offset)

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
