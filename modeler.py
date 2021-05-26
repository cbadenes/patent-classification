#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 19 20:42:09 2021

@author: cbadenes
"""

import requests
from requests.auth import HTTPBasicAuth



model_name = 'uspto-ipc-sections'
email = input("email:")
docker_pwd = input("docker password:")
docker_user = input("docker user:")

docker_credentials = {
    'email':email,
    'password':docker_pwd,
    'user': docker_user,
    'repository': docker_user + "/" + model_name
    }

data_fields = {
    'id':'id',
    'text':['abstract_t','title_t','description_t'],
    'labels':['ipc_sections']
    }

data_source = {
    'name':'uspo-patents',
    'dataFields':data_fields,
    "filter":"abstract_t:[* TO *] AND description_t:[* TO *] AND claims_t:[* TO *] AND ipc_sections:[* TO *]",
    "format": "SOLR_CORE",
    "offset": 1000,
    "size": -1,
    "url": "http://librairy-repo:8983/solr/documents"
    }

parameters = {
    "maxdocratio": "0.8",
    "lowercase" : "true",
    "minfreq": "20",
    "multigrams": "false",
    "retries":"0",
    "seed":"1066",
    "alpha": "0.1",
    "beta":"0.01",
    "iterations":"1000",
    "stopwords":""
    }

json_content = {
    'name':model_name,
    'description': 'International Patent Classification Section Codes',
    'contactEmail':email,
    'version':'latest',
    'parameters':parameters,
    'docker':docker_credentials,
    'dataSource':data_source
}

res = requests.post('http://localhost:8081/topics', json=json_content, auth=HTTPBasicAuth('basf', '2021'))
if res.ok:
    print("Response ok:",res.json())
else:
    print("Response error:",res)