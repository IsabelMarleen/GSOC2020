#Setup
import sbol2
from sbol2 import *


#Create SBOL document
doc = Document()

#Define SBOL object and components
GFP = ComponentDefinition('GFP', BIOPAX_DNA)
doc.addComponentDefinition(GFP)
       
sequence =  """atgcgtaaaggagaagaacttttcactggagttgtcccaattcttgttgaattagatggtgatgttaatgg
gcacaaattttctgtcagtggagagggtgaaggtgatgcaacatacggaaaacttacccttaaatttatttgcactactggaaaac
tacctgttccatggccaacacttgtcactactttcggttatggtgttcaatgctttgcgagatacccagatcatatgaaacagcat
gactttttcaagagtgccatgcccgaaggttatgtacaggaaagaactatatttttcaaagatgacgggaactacaagacacgtgct
gaagtcaagtttgaaggtgatacccttgttaatagaatcgagttaaaaggtattgattttaaagaagatggaaacattcttggacac
aaattggaatacaactataactcacacaatgtatacatcatggcagacaaacaaaagaatggaatcaaagttaacttcaaaattagac
acaacattgaagatggaagcgttcaactagcagaccattatcaacaaaatactccaattggcgatggccctgtccttttaccagacaa
ccattacctgtccacacaatctgccctttcgaaagatcccaacgaaaagagagaccacatggtccttcttgagtttgtaacagctgct
gggattacacatggcatggatgaactatacaaataataa"""

GFP_seq = Sequence('GFP_seq', sequence, SBOL_ENCODING_IUPAC)
doc.addSequence(GFP_seq)

LacY = ComponentDefinition('LacY', BIOPAX_DNA)
doc.addComponentDefinition(LacY)
       
sequence2 =  """atgtctgcccgtatttcgcgtaaggaaatccattatgtactatttaaaaaacacaaacttttg
gatgttcggtttattctttttcttttacttttttatcatgggagcctacttcccgtttttcccgatttggctacatgacatcaaccata
tcagcaaaagtgatacgggtattatttttgccgctatttctctgttctcgctattattccaaccgctgtttggtctgctttctgacaa
actcgggctgcgcaaatacctgctgtggattattaccggcatgttagtgatgtttgcgccgttctttatttttatcttcgggccactgt
tacaatacaacattttagtaggatcgattgttggtggtatttatctaggcttttgttttaacgccggtgcgccagcagtagaggcatt
tattgagaaagtcagccgtcgcagtaatttcgaatttggtcgcgcgcggatgtttggctgtgttggctgggcgctgtgtgcctcgatt
tcggcatcatgttcaccatcaataatcagtttgttttctggctgggctctggctgtgcactcatcctcgccgttttactctttttcgcc
aaaacggatgcgccctcttctgccacggttgccaatgcggtaggtgccaaccattcggcatttagccttaagctggcactggaactgtt
cagacagccaaaactgtggtttttgtcactgtatgttattggcgtttcctgcacctacgatgtttttgaccaacagtttgctaatttc
tttacttcgttctttgctaccggtgaacagggtacgcgggtatttggctacgtaacgacaatgggcgaattacttaacgcctcgatta
tgttctttgcgccactgatcattaatcgcatcggtgggaaaaacgccctgctgctggctggcactattatgtctgtacgtattattggc
tcatcgttcgccacctcagcgctggaagtggttattctgaaaacgctgcatatgtttgaagtaccgttcctgctggtgggctgcttta
aatatattaccagccagtttgaagtgcgtttttcagcgacgatttatctggtctgtttctgcttctttaagcaactggcgatgatttt
tatgtctgtactggcgggcaatatgtatgaaagcatcggtttccagggcgcttatctggtgctgggtctggtggcgctgggcttcacc
ttaatttccgtgttcacgcttagcggccccggcccgctttccctgctgcgtcgtcaggtgaatgaagtcgcttaa"""

LacY_seq = Sequence('LacY_seq', sequence2, SBOL_ENCODING_IUPAC)
doc.addSequence(LacY_seq)


promoter = doc.componentDefinitions['GFP']
cds = doc.componentDefinitions['LacY']


#Composition
composition_component = doc.componentDefinitions.create("composition_component")
#composition_component.assemblePrimaryStructure(['https://synbiohub.org/public/igem/BBa_K1499503/1', 'https://synbiohub.org/public/igem/BBa_K1499503/1'])
composition_component.assemblePrimaryStructure([promoter, cds])
for cd in composition_component.getPrimaryStructure():
    print(cd.displayId)
    
nucleotides = composition_component.compile()
print (nucleotides)
seq = composition_component.sequence
print(seq.elements)

composition_component.roles = [SO_GENE]

#Export
doc.write('SBOL_example.xml')




