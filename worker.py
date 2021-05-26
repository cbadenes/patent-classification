#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 19 17:52:05 2021

@author: cbadenes
"""
from bs4 import BeautifulSoup
import requests
from requests.auth import HTTPBasicAuth
  
filename =  'input/ipg210518.xml'

ipc_section_names = {
    'A':'HUMAN-NECESSITIES',
    'B':'TRANSPORTING',
    'C':'CHEMISTRY-METALLURGY',
    'D':'TEXTILES',
    'E':'FIXED-CONSTRUCTIONS',
    'F':'MECHANICAL-ENGINEERING',
    'G':'PHYSICS',
    'H':'ELECTRICITY'
}
  
def escape(text):
    return text.replace("\n"," ").replace("'","").strip()

def create_document(patent):
    doc = {}
    try:
      # Skip if it doesn't exist
      if patent is None or patent == "":
        return doc
    
      # Load patent text as HTML document
      bs = BeautifulSoup(patent, 'lxml')                                     
  
      # Search patent for application 
      application = bs.find('us-patent-application')
  
      # If no application, search for grant
      if application is None: 
        application = bs.find('us-patent-grant')
      
      # Title
      title = bs.find('invention-title').text
      doc['title_s'] = title
      
      # Id
      doc['id'] = bs.find('document-id').text.split("\n")[2]
      
      # Date
      date = bs.find('publication-reference').find('date').text 
      doc['publication_date_dt'] = date[:4]+"-"+date[4:6]+"-"+date[6:8]+"T00:00:00Z"
      
      doc['reference_s'] = bs.find('application-reference')['appl-type']

      # IPC
      categories = {}
      for classes in bs.find_all('classifications-ipcr'):
          for el in classes.find_all('classification-ipcr'):
              section = el.find('section').text
              if (section not in categories):
                  categories[section] = []
              code = el.find('class').text + el.find('subclass').text
              if (code not in categories[section]):
                  categories[section].append(code)
      if (len(categories)>0):
        doc['ipc_sections']=[ipc_section_names[section] for section in list(categories.keys())]
        for category in categories.keys():
            doc['ipc_'+category+'_codes']=categories[category]
            
      # Inventors      
      inventors = []
      for parties in bs.find_all('parties'):
          for applicants in parties.find_all('applicants'):
              for el in applicants.find_all('addressbook'):
                  inventors.append(el.find('first-name').text 
                                   + "_" + el.find('last-name').text)
      if (len(inventors)>0):
          doc['inventors']=inventors
            
      # Abstract
      abstracts = []
      for el in bs.find_all('abstract'):
          abstracts.append(escape(el.text))
      if (len(abstracts)>0):
          doc['abstract_t']=". ".join(abstracts)

      # Description
      descriptions = []
      for el in bs.find_all('description'):
          descriptions.append(escape(el.text))
      if (len(descriptions)>0):
          doc['description_t']=". ".join(descriptions)

      # Claims
      claims = []
      for el in bs.find_all('claim'):
          claims.append(escape(el.text)) 
      if (len(claims)>0):
          doc['claims_t']=". ".join(claims)    
         
      
      #print("Claims:",claims)
    except AttributeError as e:
        print("Missing attribute:",e)
        
    return doc


def evaluate(article):

    results = {}
    topic_codes = {'h0':[], 'h1':[], 'h2':[]}
    text = article['abstract_t'] + article['description_t'] + article['claims_t']
    topics = get_topics(text)
    topic_codes['h0'].extend(topics['hierarchy_level_0'])
    topic_codes['h1'].extend(topics['hierarchy_level_0']+topics['hierarchy_level_1'])
    topic_codes['h2'].extend(topics['hierarchy_level_0']+topics['hierarchy_level_1']+topics['hierarchy_level_2'])
                   
    # evaluate global codes
    reference_codes = article['ipc_sections']
        
           
    results['top1']=get_metrics(reference_codes,topic_codes['h0'])
    results['top2']=get_metrics(reference_codes,topic_codes['h1'])
    results['top3']=get_metrics(reference_codes,topic_codes['h2'])     

    response = { 'article_id':article['id'], 'results':results }
    return response


def get_topics(text):
    topics = {}
    topics.setdefault('hierarchy_level_0',[])
    topics.setdefault('hierarchy_level_1',[])
    topics.setdefault('hierarchy_level_2',[])
    print("getting topic distribution from uspto-ipc model")    
    try:
        response = requests.post("http://localhost:8585/classes", json = { 'text':text})
        data = response.json()
                
        for topic in data:
            if (topic['id']== 0):
                topics['hierarchy_level_0'].append(topic['name'])
            elif (topic['id']== 1):
                topics['hierarchy_level_1'].append(topic['name'])    
            else:     
                topics['hierarchy_level_2'].append(topic['name'])
    except Exception as e:
        print("Error getting topics:",e)
    return topics


def get_metrics(reference,value):
    reference_list = [str(ref) for ref in reference]
    value_list = [str(val) for val in value]
    tp = 0
    fp = 0
    fn = 0
    for result in value_list:
        if (result in reference_list):
            tp += 1
        else:
            fp += 1
    for data in reference_list:
        if (data not in value_list):
            fn += 1
    precision = 0.0
    if (tp + fp) > 0:
        precision = tp / (tp + fp)
    recall = 0.0
    if (tp + fn) > 0:
        recall = tp / (tp + fn)
    fmeasure = 0.0
    if (precision + recall) > 0:
        fmeasure = 2 * ( (precision * recall) / (precision + recall)  )
    return { 'tp': tp, 'fp': fp, 'fn': fn, 'precision': precision, 'recall': recall, 'fmeasure':fmeasure, 'ref-labels':reference, 'inf-labels':value}


















