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

path = '~/Desktop/Darpa Template.xlsx'
df = pd.read_excel (path)
print(df)

#Specify basic DNA parts out of master table
df[df.columns[0:6]]
basic_DNA_parts = df[12:37]
#Reassign index and column names
basic_DNA_parts.reset_index(drop=True, inplace=True)
basic_DNA_parts.columns = basic_DNA_parts.iloc[0]

#Create SBOL document
doc = Document()

#Define SBOL object and components
GFP = ComponentDefinition('GFP', BIOPAX_DNA)
doc.addComponentDefinition(GFP)

       
sequence =  """atgcgtaaag gagaagaact tttcactgga gttgtcccaa ttcttgttga
            attagatggt gatgttaatg ggcacaaatt ttctgtcagt ggagagggtg
            aaggtgatgc aacatacgga aaacttaccc ttaaatttat ttgcactact
            ggaaaactac ctgttccatg gccaacactt gtcactactt tcggttatgg
            tgttcaatgc tttgcgagat acccagatca tatgaaacag catgactttt
            tcaagagtgc catgcccgaa ggttatgtac aggaaagaac tatatttttc
            aaagatgacg ggaactacaa gacacgtgct gaagtcaagt ttgaaggtga
            tacccttgtt aatagaatcg agttaaaagg tattgatttt aaagaagatg
            gaaacattct tggacacaaa ttggaataca actataactc acacaatgta
            tacatcatgg cagacaaaca aaagaatgga atcaaagtta acttcaaaat
            tagacacaac attgaagatg gaagcgttca actagcagac cattatcaac
            aaaatactcc aattggcgat ggccctgtcc ttttaccaga caaccattac
            ctgtccacac aatctgccct ttcgaaagat cccaacgaaa agagagacca
            catggtcctt cttgagtttg taacagctgc tgggattaca catggcatgg
            atgaactata caaataataa"""
GFP_seq = Sequence('GFP_seq', sequence, SBOL_ENCODING_IUPAC)
doc.addSequence(GFP_seq)

#Export
doc.write('SBOL_example.xml')

basic_DNA_parts.renameindex={1: 'a'})


