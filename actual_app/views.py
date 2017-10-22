# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse, JsonResponse
import json, os
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth


class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'index.html', context=None)


def elastic_search(request):
	es = Elasticsearch(
        hosts=[{'host': host, 'port': 443}],
        use_ssl=True,
        http_auth=awsauth,
        verify_certs=True,
        connection_class=RequestsHttpConnection
        )
	keyword = str(request.GET.keys()[0].strip('"'))
	if keyword== "":
		data = es.search(index="index2",size=4000, body={"query": {"match_all":{}}}) 
	else:
		data = es.search(index="index2",size=4000, body={"query": {"match": {"text": keyword}}})
	loc = []
	for hit in data['hits']['hits']:
		try:
			if hit['_source']['coordinate']:
				loc.append(hit['_source']['coordinate'])
			else:
				loc.append(hit['_source']['coordinates'])
		except:
			continue
	es.indices.delete(index='index2', ignore=[400, 404])
	response_json = json.dumps(loc)
	print response_json
	return HttpResponse(response_json, content_type="application/json")



