#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 20 00:43:44 2021

@author: cbadenes
"""

import worker as workers
import pysolr
import multiprocessing as mp
import json
import time

if __name__ == '__main__':  

    # Create a client instance. The timeout and authentication options are not required.
    solr = pysolr.Solr('http://localhost:8983/solr/documents', always_commit=True, timeout=50)
        
    
    # print report
    f = open('results.jsonl', mode='w')
    print("Number of processors: ", mp.cpu_count())
    pool = mp.Pool(mp.cpu_count())
    
    
    sentences = []
    print("reading from solr..")
    counter = 0
    completed = False
    window_size=50
    cursor = "*"
    max_size=1000
    t = time.time()
    while (not completed):
        old_counter = counter
        solr_query="abstract_t:[* TO *] AND description_t:[* TO *] AND claims_t:[* TO *] AND ipc_sections:[* TO *]"
        try:            
            articles = solr.search(q=solr_query,rows=window_size,cursorMark=cursor,sort="id asc")
            cursor = articles.nextCursorMark
            results = pool.map(workers.evaluate,articles.docs)            
            for result in results:
                doc = result['article_id']
                doc_results = result['results']           
                for strategy in doc_results.keys():
                   eval_result = doc_results[strategy]
                   row = { 'doc':doc, 'strategy':strategy, 'tp':eval_result['tp'], 'fp':eval_result['fp'], 'fn':eval_result['fn'], 'precision':eval_result['precision'], 'recall':eval_result['recall'], 'fmeasure':eval_result['fmeasure'], 'ref-labels':eval_result['ref-labels'], 'inf-labels':eval_result['inf-labels']}
                   f.write(json.dumps(row))
                   f.write("\n")
            counter += len(results)
            print(counter,"docs evaluated")            
            if (old_counter == counter) or (counter>= max_size):
                print("done!")
                break            
        except Exception as e:
            print("Error:", e)
    f.close()
    print('Time to evaluate docs: {} mins'.format(round((time.time() - t) / 60, 2)))