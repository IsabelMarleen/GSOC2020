#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 24 18:33:56 2020

@author: isapoetzsch
"""

#Setup
import pandas as pd
import os
import sbol
from sbol import Document
from sbol import Component

#Read in Excel file
cwd = os.getcwd() #get current working directory
path = os.path.join(cwd, "Desktop", "darpa_template_blank.xlsx")
path2 = os.path.join(cwd, "Desktop", "darpa_template.xlsx")
blank_table = pd.read_excel (path, sheet_name = "Library", header=None)
filled_table = pd.read_excel (path2, sheet_name = "Library", header=None)

#Remove NA values
blank_table.fillna("0", inplace = True)
filled_table.fillna("0", inplace = True)

#Create a dict
library_fixed = {
    "Metadata" : blank_table.loc[[ 0,1,2,3,4,5,6,7 ], [ 0 ]] ,
    "Design Description" : blank_table.loc[[ 9 ], [ 0 ]],
    "Parts" : blank_table.loc[[ 13 ], [ 0,1,2,3,4,5]]
    }

library_filled = {
    "Metadata" : filled_table.loc[[ 0,1,2,3,4,5,6,7 ], [ 0 ]],
    "Design Description" : blank_table.loc[[ 9 ], [ 0 ]],
    "Parts" : filled_table.loc[[ 13 ], [ 0,1,2,3,4,5]]
    }


print( library_fixed == library_filled)


# #Specify basic DNA parts out of master table
# df[df.columns[0:6]]
# basic_DNA_parts = df[12:37]
# #Reassign index and column names
# basic_DNA_parts.reset_index(drop=True, inplace=True)
# basic_DNA_parts.columns = basic_DNA_parts.iloc[0]
# basic_DNA_parts = basic_DNA_parts.drop([0])
# #Line to remove space in part name strings to avoid error when using that name 
# #when defining components
# #basic_DNA_parts['Part Name'] = basic_DNA_parts['Part Name'].map(basic_DNA_parts['Part Name'].replace, [' '], ['_'])

#Create SBOL document
doc = Document()

#Define SBOL object and components
#Not yet functional because blanks in Part Name column
molecule_type = BIOPAX_DNA
component = GFP

for component in basic_DNA_parts['Part Name']: 
    component = ComponentDefinition(component, molecule_type)


