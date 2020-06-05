#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 24 18:33:56 2020

@author: isapoetzsch
"""

#Setup
import pandas as pd
import os
import logging
import sbol
from sbol import Document
from sbol import Component

#Create Template
#Read in Excel file
cwd = os.getcwd() #get current working directory
path = os.path.join(cwd, "Documents", "Utah 2020", "GSoC", "GSOC2020", "darpa_template_blank.xlsx")
path2 = os.path.join(cwd, "Documents", "Utah 2020", "GSoC", "GSOC2020", "darpa_template.xlsx")
blank_table = pd.read_excel (path, sheet_name = "Library", header=None)

#Replace NA values
blank_table.fillna("0", inplace = True)

#Create dict
library_fixed = {
    "Metadata" : blank_table.loc[[ 0,1,2,3,4,5,6,7 ], [ 0 ]].values.tolist() ,
    "Design Description" : blank_table.loc[[ 9 ], [ 0 ]].values.tolist(),
    "Parts" : blank_table.loc[[ 13 ], [ 0,1,2,3,4,5]].values.tolist()
    }


#Read in filled in spreadsheet
def readspreadsheet( path ):
   "the function reads and formats an excel spreadsheet"
   #Read function
   filled_table = pd.read_excel (path, sheet_name = "Library", header=None)
   #Replace NA
   filled_table.fillna("0", inplace = True)
   print(type(filled_table))
   return [filled_table]

def createdict (df):
    "the function creates a dictionary from a pandas df"
    #Create dict
    library_filled = {
    "Metadata" : df.loc[[ 0,1,2,3,4,5,6,7 ], [ 0 ]].values.tolist(),
    "Design Description" : df.loc[[ 9 ], [ 0 ]].values.tolist(),
    "Parts" : df.loc[[ 13 ], [ 0,1,2,3,4,5]].values.tolist()
    }
    return library_filled

filled_table = readspreadsheet(path2)
#Convert into dataframe before problem with function is fixed
filled_table = filled_table[0]
library_filled = createdict(filled_table)



#Compare spreadsheet to template to see if template has been corrupted
print( library_fixed == library_filled)

#Logging errors if spreadsheet doesn't follow template
if library_fixed != library_filled:
    logging.warning('The template spreadsheet has been corrupted')
else:
    print("Bohoo")
    

#Create SBOL document
doc = Document()

#Define SBOL object and components
#Not yet functional because blanks in Part Name column
molecule_type = BIOPAX_DNA
component = GFP

for component in basic_DNA_parts['Part Name']: 
    component = ComponentDefinition(component, molecule_type)


