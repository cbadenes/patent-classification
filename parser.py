#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 19 17:45:05 2021

@author: cbadenes
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  6 14:57:08 2021

@author: cbadenes
"""
import worker as workers
import pysolr
import multiprocessing as mp
import html
import time
import sys

if __name__ == '__main__':  

    # Create a client instance. The timeout and authentication options are not required.
    solr = pysolr.Solr('http://localhost:8983/solr/documents', always_commit=True, timeout=50)
        
    
    if (len(sys.argv) != 2):
        print("usage: python parser.py <input_file>")
        sys.exit(2)
    file        = sys.argv[1]
    
    
    # Load USPTO .xml document
    xml_text = html.unescape(open(file, 'r').read())
    	
    # Split out patent applications / grants
    counter = 0
    
    patents = xml_text.split("<?xml version=\"1.0\" encoding=\"UTF-8\"?>")

    print("Number of processors: ", mp.cpu_count())
    pool = mp.Pool(mp.cpu_count())
   
    max_length = len(patents)
    increment = 100
    min_idx = 0
    max_idx = increment
    t = time.time()
    while(min_idx<max_length):
        print("indexing",max_idx,"patents..")
        results = pool.map(workers.create_document,patents[min_idx:max_idx] )
        min_idx = max_idx
        max_idx = min_idx + increment
        valid_docs = [doc for doc in results if len(doc)>0]
        print("Size:",len(valid_docs))
        solr.add(valid_docs)
    
    pool.close()
    print('Time to parse patents: {} mins'.format(round((time.time() - t) / 60, 2)))
   
        
    
    
    
    
    
    
    
    
    
    