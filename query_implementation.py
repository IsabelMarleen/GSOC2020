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
sparql_query = fl.read()

def sparqling(sparql_query, libraries, is_basic = True, 
              no_sequence = False, progress = True):
    all_pages = []

    #loops over all pages and extracts query results
    for library in libraries:

        query_text = sparql_query.replace("library_variable", 
                        f"'{library}'")
        
        #r = requests.post(instance+"sparql", data = {"query":query_text}, 
        #                  headers = {"Accept":"application/json"})

        #d = json.loads(r.text)
        #a = json_normalize(d['results']['bindings'])

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
        # query_text = query_text.replace(f"'{library}'", 
        #                                      "library_variable")
        
    #create pandas data frame containing all page info
    #print(pd.DataFrame(all_pages))
    all_pages = pd.concat(all_pages)
    return(all_pages)


result_df = sparqling(sparql_query, list(libraries.loc["Libraries"].dropna()))
