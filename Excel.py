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
import sbol #I am working with sbol2, was that not able to install?
from sbol import Document, Component

#Create Template
#Read in Excel file
cwd = os.path.dirname(os.path.realpath(__file__)) #get current working directory - updated it for newer python version

path = os.path.join(cwd, "darpa_template_blank.xlsx") #give this a more descriptitve name e.g. blank_template_path
path2 = os.path.join(cwd, "darpa_template.xlsx") #give this a more descriptitve name e.g. filled_template_path

blank_table = pd.read_excel (path, sheet_name = "Library", header=None)

#Replace NA values
blank_table.fillna("0", inplace = True) #I don't think this is necesssary to do it is generally better to keep nans, if it is
#getting in the way of your == statement as nan is not equal to nan use: a==b|isnan(a) this means a==b or a is nan. If the type is giving
#issues try a.isnan or another variation (depends on if you are using a pandas cell, number, etc)

#Create dict - due to the excel and not csv it is not necessary to create a dictionary, I would just leave this
#it could be more efficient to use a dictionary but that would only make sense if you were reading in using xlrd instead of python
#additionally, I would have created separate dictionaries and more along the lines of:
#parts_df = blank_table.iloc[14:,0:6] #selecting only columns and rows containing parts
#parts_df.columns = blank_table.iloc[13,0:6] #setting column headers correctly
#parts_df.set_index('part name', drop=True, inplace=True) #partname is now the index rather than a column in the table
#parts = parts_df.to_dict('index') #create a dictionary
library_fixed = {
    "Metadata" : blank_table.loc[[ 0,1,2,3,4,5,6,7 ], [ 0 ]].values.tolist() ,
    "Design Description" : blank_table.loc[[ 9 ], [ 0 ]].values.tolist(),
    "Parts" : blank_table.loc[[ 13 ], [ 0,1,2,3,4,5]].values.tolist()
    }


#Read in filled in spreadsheet
def read_spreadsheet( path ): #adding an underscore makes it conform to the python standard
   #I would read in the spreadsheet in two separate parts the metadata vs the parts e.g.:
   # start_row = 13
   # use_cols = [0,1]
   # basic_DNA_parts = pd.read_excel (path, sheet_name = "Library",
   #                              header= 0, skiprows = start_row)
   #
   #metadata = pd.read_excel (path, sheet_name = "Library",
   #                              header= None, nrows = 8, usecols = use_cols)
    
   "the function reads and formats an excel spreadsheet"
   #Add a proper docustring here by typing """ - spyder should then offer to set up a docustring template for you
   #you can access the docustring by writing in the console: help(read_spreadsheet)
   #Read function
   filled_table = pd.read_excel (path, sheet_name = "Library", header=None)
   #Replace NA
   filled_table.fillna("0", inplace = True) #again I don't think this is necessary
   print(type(filled_table))
   return (filled_table) #by adding the [ brackets it makes a list containing the dataframe, round brackets should fix this

def createdict (df): #I would not create a dictionary
    "the function creates a dictionary from a pandas df"
    #Create dict
    library_filled = {
    "Metadata" : df.loc[[ 0:8 ], [ 0 ]].values.tolist(), #if you were to do it this way use a range rather than a full list
    "Design Description" : df.iloc[9, 0].values.tolist(), #additionally .loc is for names vs .iloc is for indices so if you are using numbers and not names do it like this
    "Parts" : df.iloc[13, 0:6].values.tolist() #NB: for a range it is this:upto but not including that
    }
    return library_filled

filled_table = readspreadsheet(path2) #I would read in both templates: filled and unfilled, using this function (it will make the code easier to follow)
#Convert into dataframe before problem with function is fixed
filled_table = filled_table[0]
library_filled = createdict(filled_table)


#I would do the error checking on the whole spreadsheet before doing any further processing
#Compare spreadsheet to template to see if template has been corrupted
print( library_fixed == library_filled) #if you are using dataframes this will no longer work
#for dataframes consider error checking with code along the lines of:
#comparison = np.where((filled_template == blank_template)|(blank_template.isna()), True, False)
#have a look at comparison, comparison.any(), and comparison.all()

#Logging errors if spreadsheet doesn't follow template
if library_fixed != library_filled:
    logging.warning('The template spreadsheet has been corrupted') #I would log this as an error not a warning
else: # you don't necessarily need an else here, but I am not sure what you might plan to do with it in future
    print("Bohoo")
    

#Create SBOL document
doc = Document()

#Define SBOL object and components
#Not yet functional because blanks in Part Name column
molecule_type = BIOPAX_DNA
component = GFP

for component in basic_DNA_parts['Part Name']: 
    component = ComponentDefinition(component, molecule_type)


