from requests_aws4auth import AWS4Auth
from elasticsearch import Elasticsearch, RequestsHttpConnection
import boto3
import json


es = Elasticsearch()

data = es.search(index="tweet_file", size=10000, body={"query": {"match_all": {}}})

for hit in data['hits']['hits']:
	try:
		if(hit['_source']['coordinates']==True):
			print hit['_source']['coordinates']
		else:
			print hit['_source']['coordinate']
	except:
		continue


	




