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
path_blank = os.path.join(cwd, "darpa_template_blank.xlsx")
path_filled = os.path.join(cwd, "darpa_template.xlsx")


#Read in template and filled spreadsheet
def read_spreadsheet(path, start_row, nrows, use_cols):
    """
    the function reads and formats an excel spreadsheet based on the Darpa template.
    It requires a sheet with the name "Library".
    
    Requires
    --------
    import pandas as pd

    Parameters
    ----------
    path : STRING
        Path to Excel Spreadsheet
    start_row : INTGER
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
    #add error catching if the sheet Library doesn't exist? Should Library be a variable and not hardcoded?
    basic_DNA_parts = pd.read_excel (path, sheet_name = "Library",
                                  header= 0, skiprows = start_row)
    
    metadata = pd.read_excel (path, sheet_name = "Library",
                                  header= None, nrows = nrows, usecols = use_cols)
    
    return (basic_DNA_parts, metadata)

filled_data, filled_metadata = readspreadsheet(path_filled,  
                start_row = 13, nrows = 8, use_cols = [0,1])
blank_data, blank_metadata = readspreadsheet(path_blank,  
                start_row = 13, nrows = 8, use_cols = [0,1])


#Quality control spreadsheet
comparison = np.where((filled_metadata == blank_metadata)|(blank_metadata.isna()), True, False)
if not(comparison.all()) :
    logging.warning("Some cells do not match the template")
    temporary = "xyz"
    logging.warning(f"The cells that do not match are {temporary}")

filled_columns = set(filled_data.columns)
blank_columns = set(blank_data.columns)

if not(blank_columns.issubset(filled_columns)) :
    logging.warning("Some of the required columns are missing")


#Create SBOL document
doc = Document()

#Define SBOL object and components
molecule_type = BIOPAX_DNA #Change later

for index, row in filled_data.iterrows():
    component = ComponentDefinition(row["Part Name"], molecule_type)
    doc.addComponentDefinition(component)
    
    sequence = Sequence(f"{row['Part Name']}_sequence", row["Sequence"], SBOL_ENCODING_IUPAC)
    doc.addSequence(sequence)

doc.write('SBOL_example.xml')


