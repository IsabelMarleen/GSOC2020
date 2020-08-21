#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 14:57:34 2020

@author: isapoetzsch
"""
#Set up
import pandas as pd
import numpy as np
import os
import logging
from col_to_excel import col_to_excel
import sbol2
from sbol2 import Document, PartShop
import re

cwd = os.path.dirname(os.path.abspath("__file__")) #get current working directory
path_filled = os.path.join(cwd, "darpa_template.xlsx")
path_blank = os.path.join(cwd, "templates/darpa_template_blank.xlsx")

#read in the whole sheet below metadata
startrow_composition = 9
sheet_name = "Composite Parts"
table = pd.read_excel (path_filled, sheet_name = sheet_name, 
                       header = None, skiprows = startrow_composition)

#Load Metadata and Quality Check
nrows = 8
use_cols = [0,1]
filled_composition_metadata = pd.read_excel (path_filled, sheet_name = sheet_name,
                              header= None, nrows = nrows, usecols = use_cols)
blank_composition_metadata = pd.read_excel (path_blank, sheet_name = sheet_name,
                              header= None, nrows = nrows, usecols = use_cols)
 
comparison = np.where((filled_composition_metadata == blank_composition_metadata)|(blank_composition_metadata.isna()), True, False)
excel_cell_names = []
for column in range(0, len(use_cols)):
    for row in range(0, comparison.shape[0]):
        col = use_cols[column]
        excel_cell_names.append(f"{col_to_excel(col+1)}{row+1}")
excel_cell_names = np.reshape(excel_cell_names, comparison.shape, order='F')
excel_cell_names = pd.DataFrame(excel_cell_names)
excel_cell_names.where(np.logical_not(comparison))

if not(comparison.all()) :
    logging.warning("Some cells do not match the template")
    for number in range(0, nrows-1) :
        if filled_composition_metadata.iloc[number, 0] != blank_composition_metadata.iloc[number, 0]:
            logging.warning(f"""The excel cell {excel_cell_names.loc[number, 0]} has been corrupted and 
                  should contain {blank_composition_metadata.iloc[number, 0]}""")
          

#Load Libraries required for Parts
libraries = dict()
if table.iloc[0][0] == "Libraries" and table.iloc[0][1] == "Abbreviations":
    for index, row in table.iloc[1:len(table)].iterrows():
        if row[0] == "Composite DNA Parts" or row.dropna().empty: 
            break
        else:
            #if there is no abbreviation, use full name as key
            if not pd.isnull(table.iloc[index][1]):
                libraries[table.iloc[index][1]] = table.iloc[index][0]
            else:
                libraries[table.iloc[index][0]] = table.iloc[index][0]


#Loop over all rows and find those where each block begins
compositions = dict()
all_parts = []
labels = np.array(["Collection Name:", "Name:", "Description:", "Strain (optional)",
          "Integration Locus (optional)", "Part Sequence:"])
for index, row in table.iterrows():
    #identifies set of six rows in table where first column matches the labels
    labs = np.asarray(table.iloc[index : index+6][0])
    comparison = labs == labels 
    
    if row[0] == "Collection Name:" and comparison.all() :
        #check if collection name exists in a previous block if so add to that dictionary or if not
        #create a new one
        try:
            collection_dict = compositions[table.iloc[index][1]]
        except:
            collection_dict = {}
            
        for column in range(1,5):
            if type(table.iloc[index+1][column]) is str: #check if name is not empty
                collection_dict[table.iloc[index+1][column]] = {"Description" : {table.iloc[index+2][column]},
                                                                "Parts" : {}}
                
                parts = table.iloc[index+5: len(table)][column].dropna()
                print(parts)
                
                # if len(parts) == 0:
                #     logging.warning(f"The collection {compositions[value]} was empty and thus removed")
                #     del compositions[value]
                #     list_of_rows.remove(value)
                
               # else:
                collection_dict['Parts'] = parts.tolist()
                all_parts+=collection_dict["Parts"]
                
        compositions[table.iloc[index][1]] = collection_dict
    else:
        names = table.iloc[index: index+6][0].tolist()
    

    #Extract part names from compositions   
    for column in range(1,5):
     #   for index, value in enumerate(list_of_rows):
           # if index == len(list_of_rows)-1:
        collection_dict[table.iloc[index+1][column]]['Parts'] = table.iloc[index+5: len(table)][column].dropna()
            # else:
            #     print(parts)
            #     parts = table.iloc[value+5: list_of_rows[index+1]][column].dropna()
        # if len(parts) == 0:
        #     logging.warning(f"The collection {compositions[value]} was empty and thus removed")
        #     # del compositions[value]
        #     # list_of_rows.remove(value)
                
       # else:
        # collection_dict[column]['Parts'] = parts.tolist()
        # all_parts+=collection_dict[column]["Parts"]
            
all_parts = set(all_parts) #set eliminates duplicates




#Check if Collection names are alphanumeric and separated by underscore
for index, value in enumerate(list_of_rows):
    old = compositions[value]['Collection Name'] #for error warning
    title = compositions[value]['Collection Name'].replace('_', '') #remove underscore to use isalnum()
    if title.isalnum():
        print(f"Collection name {compositions[value]['Collection Name']} is valid")
    else: #replace special characters with numbers
        for letter in title:
            if ord(letter) > 122:
                #122 is the highest decimal code number for common latin letters or arabic numbers
                #this helps identify special characters like ä or ñ, which isalnum() returns as true
                #the characters that don't meet this criterion are replaced by their decimal code number separated by an underscore
                compositions[value]['Collection Name'] = compositions[value]['Collection Name'].replace(letter, str( f"_{ord(letter)}"))
            else:
                letter = re.sub('[\w, \s]', '', letter) #remove all letters, numbers and whitespaces
                #this enables replacing all other special characters that are under 122
                if len(letter) > 0:
                    compositions[value]['Collection Name'] = compositions[value]['Collection Name'].replace(letter, str( f"_{ord(letter)}"))
        print(f"Collection name {old} was not valid and replaced by {compositions[value]['Collection Name']}")


doc = Document()

for library in libraries:
   # sbol2.setHomespace('http://sys-bio.org')
    library = sbol2.PartShop(libraries[library])
    for part in all_parts:
        print(part)
        library.pull(part, doc)

# bsu = 'https://synbiohub.org/public/bsu'
# bsu = sbol2.PartShop(bsu)
# for part in all_parts:
#     print(part)
#     bsu.pull(part, doc)
    

#bsu.pull('BO_32977', doc)
#'BBa_E0040', 'BBa_I719005', 'BBa_M36010', 'BBa_R0040'
    
    
# GSOC_SBH_URL = 'https://synbiohub.org'
# collection = 'https://synbiohub.org/public/igem/igem_collection/1'
# display_id = 'BBa_E0040'
# query = sbol2.SearchQuery()
# query[sbol2.SBOL_COLLECTION] = collection
# query[sbol2.SBOL_DISPLAY_ID] = display_id
# # GSOC is always looking for DNA Region
# query[sbol2.SBOL_TYPES] = sbol2.BIOPAX_DNA
# part_shop = sbol2.PartShop(GSOC_SBH_URL)
# response = part_shop.search(query)
# # At least one item in return should be the
# # expected return: https://synbiohub.org/public/igem/BBa_E0040/1
# identities = [r.identity for r in response]
# # self.assertIn('https://synbiohub.org/public/igem/BBa_E0040/1', identities)
# # #
# # # All items in response should have name == GFP exactly.
# # display_ids = [r.displayId == display_id for r in response]
# # self.assertTrue(all(display_ids))




# rbs = doc.componentDefinitions['BBa_E0040']
# cds = doc.componentDefinitions['BBa_I719005']
# ppp = doc.componentDefinitions['BBa_R0040']


#for key, value in compositions.items():
#    print(value["Parts"])


# Create a new empty device named `my_device`

# Create a new empty device named `my_device`
composition_component= doc.componentDefinitions.create('composition_component')
composition_component.assemblePrimaryStructure(list(all_parts))
# for c in composition_component.getPrimaryStructure():
#     print(cd.displayId)
    
# nucleotides = composition_component.compile()
# print (nucleotides)
# seq = composition_component.sequence
# print(seq.elements)

# composition_component.roles = [SO_GENE]



