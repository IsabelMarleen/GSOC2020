#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 14:57:34 2020

@author: isapoetzsch
"""
#Playground
import pandas as pd
import numpy as np
import os
import logging
import col_to_excel
from col_to_excel import col_to_excel
import sbol2
from sbol2 import Document, Component, ComponentDefinition
from sbol2 import BIOPAX_DNA, Sequence, SBOL_ENCODING_IUPAC
from sbol2 import ModuleDefinition


cwd = os.path.dirname(os.path.abspath("__file__")) #get current working directory
path_blank = os.path.join(cwd, "darpa_template_blank.xlsx")
path_filled = os.path.join(cwd, "darpa_template.xlsx")

#read in the whole sheet
table = pd.read_excel (path_filled, sheet_name = "Composite Parts", header = None) # below metadata

#Loop over all rows and find those where each block begins
list1 = []
d = dict()
labels = np.array(["Collection Name:", "Name:", "Description:", "Strain (optional)",
          "Integration Locus (optional)", "Part Sequence:"])
for index, row in table.iterrows():
    comparison = np.asarray(table.iloc[index : index+6][0]) == labels
    if row[0] == "Collection Name:" and comparison.all() :
        list1.append(index)    
        d[index] = {"Collection Name": table.iloc[index][1],
                    "Name" : table.iloc[index+1][1],
                    "Parts": {} }
    else:
        names = table.iloc[index: index+6][0].tolist()



all_parts = []
     
for index, value in enumerate(list1):
    if index == len(list1)-1:
        parts = table.iloc[value+5: len(table)][1].dropna()
    else:
        parts = table.iloc[value+5: list1[index+1]][1].dropna()
    
    if len(parts) == 0:
        del d[value]
    else:
        d[value]['Parts'] = parts.tolist()
        all_parts+=d[value]["Parts"] #turn into set to avoid duplicates after for loop
        
all_parts = set(all_parts)
    
#for key, value in d.items():
#    print(value["Parts"])


#doc = Document()
# template = ModuleDefinition('template')
# template = template.assemble([])
# template = template.assemble([GFP, tetR, M36010] )
# doc.addModuleDefinition(template)
# doc.GFP
