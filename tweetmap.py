try:
    import json
except ImportError:
    import simplejson as json

from twitter import *
from requests_aws4auth import AWS4Auth
from elasticsearch import Elasticsearch, RequestsHttpConnection
import boto3
import json

es = Elasticsearch(
        hosts=[{'host': host, 'port': 443}],
        use_ssl=True,
        http_auth=awsauth,
        verify_certs=True,
        connection_class=RequestsHttpConnection
        )
print es.info()

t = Twitter(auth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET))
twitter_stream = TwitterStream(auth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET))
iterator = twitter_stream.statuses.sample()

for tweet in iterator:
    try:
        if 'text' in tweet:
            if tweet['coordinates']:
                coordinates = tweet['coordinates']['coordinates']
                es.index(index='index2', doc_type='tweet', body={'text': tweet['text'].lower().encode('ascii','ignore').decode('ascii'), 'coordinates': coordinates})
                print "xyz"
            elif 'place' in tweet.keys() and tweet['place']:
                coordinate = tweet['place']['bounding_box']['coordinates'][0][0]
                es.index(index='index2', doc_type='tweet', body={'text': tweet['text'].lower().encode('ascii','ignore').decode('ascii'), 'coordinate': coordinate})
                print "xyz"
    except:
        continue

	
