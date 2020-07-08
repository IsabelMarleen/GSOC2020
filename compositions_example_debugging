#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 23:16:04 2020

@author: isapoetzsch
"""


import sbol2
import os

# Set the default namespace (e.g. “http://my_namespace.org”)
sbol2.setHomespace('http://sys-bio.org')
# Create a new SBOL document
doc = sbol2.Document()
# Load some generic parts from `parts.xml` into another Document
cwd = os.path.dirname(os.path.abspath("__file__")) #get current working directory
path_parts = os.path.join(cwd, "TestCollection_collection.xml")
doc.read(path_parts)

# Inspect the Document
for obj in doc:
    print(obj.displayId, obj.type)
    

# Import the medium strength device into your document
for cd in doc.componentDefinitions:
    print(cd)
    
    
    
# Extract the medium strength promoter `Medium_2016Interlab` from your document.
promoter = doc.componentDefinitions['GFP']

# Extract the coding region (cds) `LuxR` from your document.
cds = doc.componentDefinitions['Lac_Y']


# Create a new empty device named `my_device`
my_device = doc.componentDefinitions.create('my_device')

# Assemble the new device from the promoter, rbs, cds, and terminator from above.
my_device.assemblePrimaryStructure([promoter, cds], sbol2.IGEM_STANDARD_ASSEMBLY)


# Inspect the primary structure
for cd in my_device.getPrimaryStructure():
    print(cd.displayId)
    
    
    
    
# Compile the sequence for the new device
nucleotides = my_device.compile()
seq = my_device.sequence
print(seq.elements)



# Set the role of the device with the Sequence Ontology term `gene`
my_device.roles = [sbol2.SO_GENE]


print(my_device.roles)

my_device.roles = [sbol2.SO + '0000444']

my_device.roles

