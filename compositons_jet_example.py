# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 15:39:17 2020

@author: JVM
"""

from sbol2 import *
import sbol2

setHomespace('http://sys-bio.org')
doc = Document()

gene = ComponentDefinition('gene_example')
r0010 = ComponentDefinition('R0010')
b0032 = ComponentDefinition('B0032')
e0040 = ComponentDefinition('E0040')
b0012 = ComponentDefinition('B0012')

r0010.roles = SO_PROMOTER
b0032.roles = SO_CDS
e0040.roles = SO_RBS
b0012.roles = SO_TERMINATOR

doc.addComponentDefinition(gene)
doc.addComponentDefinition([r0010, b0032, e0040, b0012])

gene.assemblePrimaryStructure([r0010, b0032, e0040, b0012])

first = gene.getFirstComponent()
print(first.identity)
last = gene.getLastComponent()
print(last.identity)

r0010.sequence = Sequence('R0010', 'ggctgca')
b0032.sequence = Sequence('B0032', 'aattatataaa')
e0040.sequence = Sequence('E0040', "atgtaa")
b0012.sequence = Sequence('B0012', 'attcga')

target_sequence = gene.compile()
print(gene.sequence.elements)

# doc.write('gene_cassette.xml')
# print(result)

# Start an interface to igem’s public part shop on SynBioHub. Located at `https://synbiohub.org/public/igem`
igem = sbol2.PartShop('https://synbiohub.org/public/igem')
# Search the part shop for parts from the iGEM interlab study using the search term `interlab`
records = igem.search('BBa_R0010')
for r in records:
    print(r)