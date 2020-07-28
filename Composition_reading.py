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
import col_to_excel
from col_to_excel import col_to_excel
import sbol2
from sbol2 import Document, Component, ComponentDefinition
from sbol2 import BIOPAX_DNA, Sequence, SBOL_ENCODING_IUPAC, PartShop
# from Excel import doc

cwd = os.path.dirname(os.path.abspath("__file__")) #get current working directory
path_filled = os.path.join(cwd, "darpa_template.xlsx")
path_blank = os.path.join(cwd, "templates/darpa_template_blank.xlsx")

#read in the whole sheet
startrow_composition = 9
sheet_name = "Composite Parts"
table = pd.read_excel (path_filled, sheet_name = sheet_name, 
                       header = None, skiprows = startrow_composition) # below metadata

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
            if not pd.isnull(table.iloc[index][1]):
                libraries[table.iloc[index][1]] = table.iloc[index][0]
            else:
                libraries[table.iloc[index][0]] = table.iloc[index][0]


#Loop over all rows and find those where each block begins
list_of_rows = []
compositions = dict()
labels = np.array(["Collection Name:", "Name:", "Description:", "Strain (optional)",
          "Integration Locus (optional)", "Part Sequence:"])
for index, row in table.iterrows():
    labs = np.asarray(table.iloc[index : index+6][0])
    comparison = labs == labels
    if row[0] == "Collection Name:" and comparison.all() :
        list_of_rows.append(index)    
        compositions[index] = {"Collection Name": table.iloc[index][1],
                    "Name" : table.iloc[index+1][1],
                    "Parts": {} }
    else:
        names = table.iloc[index: index+6][0].tolist()

#Extract part names from compositions
all_parts = []
     
for index, value in enumerate(list_of_rows):
    if index == len(list_of_rows)-1:
        parts = table.iloc[value+5: len(table)][1].dropna()
    else:
        parts = table.iloc[value+5: list_of_rows[index+1]][1].dropna()
    
    if len(parts) == 0:
        del compositions[value]
        list_of_rows.remove(value)
    else:
        compositions[value]['Parts'] = parts.tolist()
        all_parts+=compositions[value]["Parts"]
        
all_parts = set(all_parts) #set eliminates duplicates

#Check if Collection names are alphanumeric and separated by underscore
for index, value in enumerate(list_of_rows):
    print(compositions[value]['Collection Name'])
    if "_" in compositions[value]['Collection Name']:
        title = compositions[value]['Collection Name'].replace('_', '')
        if title.isalnum():
            print(f"Collection name {compositions[value]['Collection Name']} is valid")
        else:
            title.encode(errors = "replace")
            print(title)
    else:
        if title.isalnum():
            print(f"Collection name {compositions[value]['Collection Name']} is valid")
        else:
            
            title.encode('ascii','ignore')
    

doc = Document()

sbol2.setHomespace('http://sys-bio.org')
igem = sbol2.PartShop(libraries["igem"])
for part in all_parts:
    print(part)
    records = igem.pull(part, doc)
    for r in records:
        print(r)

#for key, value in compositions.items():
#    print(value["Parts"])


# doc = Document()
# composition_component = doc.componentDefinitions.create("composition_component")
# composition_component.assemblePrimaryStructure([GFP, LacY], IGEM_STANDARD_ASSEMBLY)
# for c in composition_component.getPrimaryStructure():
#     print(cd.displayId)
    
# nucleotides = composition_component.compile()
# print (nucleotides)
# seq = composition_component.sequence
# print(seq.elements)

# composition_component.roles = [SO_GENE]

