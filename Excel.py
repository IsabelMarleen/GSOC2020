#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 24 18:33:56 2020

@author: isapoetzsch
"""

#Read in Excel file
import pandas as pd
df = pd.read_excel (r'~/Downloads/Darpa Template.xlsx')
print(df)