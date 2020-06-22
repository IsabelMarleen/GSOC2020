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
from Excel import 


cwd = os.path.dirname(os.path.abspath("__file__")) #get current working directory
path_blank = os.path.join(cwd, "darpa_template_blank.xlsx")
path_filled = os.path.join(cwd, "darpa_template.xlsx")

#read in the whole sheet
table = pd.read_excel (path_filled, sheet_name = "Composite Parts", header = None)

#Loop over all rows and find those where each block begins
list1 = []
for index, row in table.iterrows():
    if row[0] == "Collection Name:":
        list1.append(index)     
#Find the difference between the beginning rows to determine the length of each block
list2 = np.diff(list1) 

#Reading in first block as example using the values determined above
table_1 = pd.read_excel (path_filled, sheet_name = "Composite Parts", 
                                      skiprows= list1[1]-1, nrows = list2[1])


#Failed attempt to automatise the table creation, 
#cannot create variables like that need to find better alternative
#for entry in list1 and value in list2:
#   exec(f'table_{entry}') = pd.read_excel (path_filled, sheet_name = "Composite Parts", 
#                                      skiprows= entry, nrows = value)