#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 24 18:33:56 2020

@author: isapoetzsch
"""

#Setup
import pandas as pd
import numpy as np
import os
import logging
import sbol2
from sbol2 import Document, Component, ComponentDefinition
from sbol2 import BIOPAX_DNA, Sequence, SBOL_ENCODING_IUPAC

cwd = os.path.dirname(os.path.abspath("__file__")) #get current working directory
cwd = os.path.join(cwd, "Documents", "Utah 2020", "GSoC", "GSOC2020")
path_blank = os.path.join(cwd, "darpa_template_blank.xlsx")
path_filled = os.path.join(cwd, "darpa_template.xlsx")


#Read in template and filled spreadsheet
def read_spreadsheet( path, start_row, nrows, use_cols ):
    """
    the function reads and formats an excel spreadsheet sheet with the name "Library"

    Parameters
    ----------
    path : STRING
        Path to Excel Spreadsheet
    start_row : INTEGER
        Defines first row to be read for the parts table
    nrows: INTEGER
        Defines number of rows to be read for the metadata section
    usecols: LIST
        Defines which columns should be read for the metadata section (note column A is 0)
    

    Returns
    -------
     basic_DNA_parts: DATAFRAME
         The parts table with headers from row=start_row and data from all rows after that.
     metadata: DATAFRAME, (usecols x nrows)
         A header less table of length nrows and width usecols
     
     Example
     -------
     cwd = os.path.dirname(os.path.abspath("__file__")) #get current working directory
     path_filled = os.path.join(cwd, "darpa_template.xlsx")
     filled_data, filled_metadata = readspreadsheet(path_filled,  
                 start_row = 13, nrows = 8, use_cols = [0,1])

    """
    basic_DNA_parts = pd.read_excel (path, sheet_name = "Library",
                                  header= 0, skiprows = start_row)
    
    metadata = pd.read_excel (path, sheet_name = "Library",
                                  header= None, nrows = nrows, usecols = use_cols)
    
    return (basic_DNA_parts, metadata)

filled_data, filled_metadata = read_spreadsheet(path_filled,  
                start_row = 13, nrows = 8, use_cols = [0,1])
blank_data, blank_metadata = read_spreadsheet(path_blank,  
                start_row = 13, nrows = 8, use_cols = [0,1])

description = pd.read_excel(path_filled, sheet_name= "Library", skiprows = 9, 
                            nrows = 1, usecols = [0])


#Quality control spreadsheet
##Load erroneaous spreadsheet for testing, temporary part
path_error = os.path.join(cwd, "darpa_template_error.xlsx")
error_data, error_metadata  = read_spreadsheet(path_error,  
                start_row = 13, nrows = 8, use_cols = [0,1])

#Description
if description.columns != "Design Description":
    logging.warning("A10 has been corrupted, it should be labelled 'Design Description'")

#Metadata
comparison = np.where((filled_metadata == blank_metadata)|(blank_metadata.isna()), True, False)
metadata_cells = pd.DataFrame(data = {"Names": blank_metadata.iloc[:, 0],"Cells": 
            ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8'] } ) #add as column to filled_metadata instead?
if not(comparison.all()) :
    logging.warning("Some cells do not match the template")
    for number in range(0,7) :
        if filled_metadata.iloc[number, 0] != blank_metadata.iloc[number, 0]:
            logging.warning(f"""The excel cell {metadata_cells.loc[number, 'Cells']} has been corrupted and 
                  should contain {blank_metadata.iloc[number, 0]}""")
                  
#Library data
filled_columns = set(filled_data.columns)
blank_columns = set(blank_data.columns)

if not(blank_columns.issubset(filled_columns)) :
    logging.warning("Required columns are missing")


#Create SBOL document
doc = Document()

#Define SBOL object and components
#Parts Library
molecule_type = BIOPAX_DNA #Change later

for index, row in filled_data.iterrows():
    component = ComponentDefinition(row["Part Name"], molecule_type)
    component.roles = row["Role"]
    doc.addComponentDefinition(component)
    
    sequence = Sequence(f"{row['Part Name']}_sequence", row["Sequence"], SBOL_ENCODING_IUPAC)
    doc.addSequence(sequence)

#Metadata
doc.description = description.iloc[0,0]
doc.name = filled_metadata.iloc[0, 1]

doc.write('SBOL_example.xml')


