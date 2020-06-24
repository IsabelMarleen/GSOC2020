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
import math
import logging
import col_to_excel
from col_to_excel import col_to_excel
import sbol2
from sbol2 import Document, Component, ComponentDefinition
from sbol2 import BIOPAX_DNA, Sequence, SBOL_ENCODING_IUPAC
from sbol2 import ModuleDefinition
from Excel import read_composition


cwd = os.path.dirname(os.path.abspath("__file__")) #get current working directory
path_blank = os.path.join(cwd, "darpa_template_blank.xlsx")
path_filled = os.path.join(cwd, "darpa_template.xlsx")

#read in the whole sheet
table = pd.read_excel (path_filled, sheet_name = "Composite Parts", header = None) # below metadata

#Loop over all rows and find those where each block begins
list1 = []
d = dict()
for index, row in table.iterrows():
    if row[0] == "Collection Name:" and table.iloc[index+1][0] == "Name:" : #add other rows, create list and check against template list
        list1.append(index)    
        d[index] = {"Collection Name": table.iloc[index][1],
                    "Name" : table.iloc[index+1][1],
                    "Parts": {} }
    #add else to find out which rows have wrong label
    else:
        names = table.iloc[index: index+6][0].tolist()
        print(names)
        
for index, value in enumerate(list1):
    if index == len(list1)-1:
        parts = table.iloc[value+5: len(table)][1].dropna()
    else:
        parts = table.iloc[value+5: list1[index+1]][1].dropna()
    
    if len(parts) == 0:
        del d[value]
    else:
        d[value]['Parts'] = parts.tolist()
    print(parts)
    
for key, value in d.items():
    print(value["Collection Name"])





doc = Document()
template = ModuleDefinition('template')
doc.addModuleDefinition(template)
