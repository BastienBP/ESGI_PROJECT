#from twitter import StdOutListener
#rom twitter import tweepy
import tweepy
import json
import os,sys
import subprocess
from kafka import KafkaProducer
import datetime

SEARCH_TERM = sys.argv[1]


with open('../params/config.json') as f:
    tokens = json.loads(f.read())
with open("../params/params.json") as f:
    data = json.load(f)
broker1 = data['cluster']['broker1']
broker2 = data['cluster']['broker2']
broker3 = data['cluster']['broker3']
server_port = data['server_port']
zookieper_port = data['zookieper_port']
consumer_key = tokens['CONSUMER_KEY']
consumer_secret = tokens['CONSUMER_SECRET']
access_token = tokens['ACCESS_TOKEN']
access_token_secret = tokens['ACCESS_SECRET']
TOPIC = data['topic']

################################################################################



def execCmd(cmd):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    retText = []
    for line in p.stdout.readlines():
        retText.append(line)
    retVal = p.wait()
    return retVal,retText

def get_producer(cluster_list):
	producer = KafkaProducer(bootstrap_servers= cluster_list)
	return producer

def produce(producer, topic, msg):
    try:
        producer.send(topic, msg, partition=0, timestamp_ms=datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f'))
        print 'Still sending to the partition 0'
    except Exception as e:
        print str(e)
        return str(e)

cmd = 'kafka-topics.sh --create --zookeeper '+broker1+':'+zookieper_port+' --replication-factor 3 --partitions 3 --topic ' + TOPIC + ' &'
t, d = execCmd(cmd)
if t is 0 and d:
	print 'Topic well created..'
if not d:
	print TOPIC + ' already created..'
print "Connection to 104.199.104.122:9092"
cluster_list = [broker1+':'+server_port,broker2+':'+server_port,broker3+':'+server_port]
producer = get_producer(cluster_list)



# This is the listener, resposible for receiving data
class StdOutListener(tweepy.StreamListener):
    def on_data(self, data):
        # Twitter returns data in JSON format - we need to decode it first
        decoded = json.loads(data)

        # Also, we convert UTF-8 to ASCII ignoring all bad characters sent by users
        #print '@%s: %s' % (decoded['user']['screen_name'], decoded['text'].encode('ascii', 'ignore'))
        print type(decoded['user']['screen_name'])
        msg = '@%s: %s' %(decoded['user']['screen_name'], decoded['text'].encode('ascii', 'ignore'))
        produce(producer, TOPIC, msg.encode())
        #decoded['user']['screen_name'].encode('ascii', 'ignore'))
        print ''
        return True

    def on_error(self, status):
        print status


if __name__ == '__main__':
    l = StdOutListener()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    print "Showing all new tweets for "+SEARCH_TERM+" :"
    # There are different kinds of streams: public stream, user stream, multi-user streams
    # In this example follow #programming tag
    # For more details refer to https://dev.twitter.com/docs/streaming-apis
    stream = tweepy.Stream(auth, l)
    # while True:
    message = stream.filter(track=[SEARCH_TERM])
    #     print "Message: "
    #     print message
    #     #produce(producer, TOPIC, )

    #print l.on_data(stream)
    #stream.filter(track=['0'.format(sys.argv[1])])
