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
from Composition_reading import libraries, all_parts

instance = "https://synbiohub.org/"
fl = open("query_select_collection.txt", "r")
sparql_query = fl.read()

def sparqling(sparql_query, libraries, is_basic = True, 
              no_sequence = False, progress = True):
    """
    the function querys "https://synbiohub.org/" for parts

    Parameters
    ----------
    path : STRING
        Path to Excel Spreadsheet
    sparql_query
    libraries
    is_basic = True, 
    no_sequence = False
    progress = True
    

    Returns
    -------
     basic_DNA_parts: DATAFRAME
         The parts table with headers from row=start_row and data from all rows after that.
     metadata: DATAFRAME, (usecols x nrows)
         A header less table of length nrows and width usecols
    description: DATAFRAME, (description_col x 1)
         A table consisting usually of a single cell and the header "Design Description"
     
     Example
     -------
     cwd = os.path.dirname(os.path.abspath("__file__")) #get current working directory
     path_filled = os.path.join(cwd, "darpa_template.xlsx")
     filled_library, filled_metadata, filled_description = read_library(path_filled,  
                 start_row = 13, nrows = 8, description_row = 9)

    """
    all_pages = []

    #loops over all pages and extracts query results
    for library in libraries:

        query_text = sparql_query.replace("library_variable", 
                        f"'{library}'")
    
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

    #create pandas data frame containing all page info
    #print(pd.DataFrame(all_pages))
    all_pages = pd.concat(all_pages)
    return(all_pages)


result_df = sparqling(sparql_query, list(libraries.loc["Libraries"].dropna()))

for part in all_parts:
    for index, row in result_df.iterrows():
        if part == row["title.value"]:
            print(part)
    
    
    
    
    partfile = requests.get(filename).content