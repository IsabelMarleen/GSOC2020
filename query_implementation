#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 17:12:23 2020

@author: isapoetzsch
"""


import requests
import json
from pandas import json_normalize
import pandas as pd
import numpy as np
from Composition_reading import libraries

instance = "https://synbiohub.org/"
fl = open("query_select_collection.txt", "r")
sparqlquery = fl.read()
query_text = sparqlquery

def sparqling(query_text, libraries, is_basic = True, 
              no_sequence = False, progress = True):
    all_pages = []

    #loops over all pages and extracts query results
    for library in libraries:

        query_text = query_text.replace("library_variable", 
                        f"'{library}'")
        
        r = requests.post(instance+"sparql", data = {"query":query_text}, 
                          headers = {"Accept":"application/json"})

        d = json.loads(r.text)
        a = json_normalize(d['results']['bindings'])

        for i in range(0,2000):
            
            if progress: #print progress
                print(i)
                
            #replace placeholder in query_text with page number to get
            queryed = query_text.replace("replacehere", str(i*10000))
            
            #make request for data
            r = requests.post("https://synbiohub.org/sparql",
                              data = {"query":queryed},
                              headers = {"Accept":"application/json"})
            
            #reformat page data
            d = json.loads(r.text)
            one_page = json_normalize(d['results']['bindings'])
            
            #add page data to all pages data
            all_pages.append(one_page)
            
            #if the page was no longer a full page stop loop
            if len(one_page)<10000:
                break
        query_text = query_text.replace(f"'{library}'", 
                                             "library_variable")
        
    #create pandas data frame containing all page info
    print(pd.DataFrame(all_pages))
    return(all_pages)


result_df = sparqling(sparqlquery, list(libraries.loc["Libraries"].dropna()))
