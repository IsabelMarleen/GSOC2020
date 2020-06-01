#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 24 18:33:56 2020

@author: isapoetzsch
"""

#Setuo
import pandas as pd
import os
import sbol
from sbol import Document
from sbol import *

#Read in Excel file
cwd = os.getcwd() #get current working directory
path = os.path.join(cwd, "Desktop", "Darpa Template.xlsx")

#path = '~/Desktop/Darpa Template.xlsx'
df = pd.read_excel (path)
print(df)

#Specify basic DNA parts out of master table
df[df.columns[0:6]]
basic_DNA_parts = df[12:37]
#Reassign index and column names
basic_DNA_parts.reset_index(drop=True, inplace=True)
basic_DNA_parts.columns = basic_DNA_parts.iloc[0]
basic_DNA_parts = basic_DNA_parts.drop([0])
#Line to remove space in part name strings to avoid error when using that name 
#when defining components
basic_DNA_parts['Part Name'].apply(basic_DNA_parts.replace( [' '], ['_']))

#Create SBOL document
doc = Document()

#Define SBOL object and components
#Not yet functional because blanks in Part Name column
molecule_type = BIOPAX_DNA

for component in basic_DNA_parts['Part Name']: 
   component = ComponentDefinition(component, molecule_type)


