#Setup
import sbol2
from sbol2 import Document
from sbol2 import *

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

LacY = ComponentDefinition('LacY', BIOPAX_DNA)
doc.addComponentDefinition(LacY)
       
sequence2 =  """﻿atgtctgccc gtatttcgcg taaggaaatc cattatgtac tatttaaaaa
            acacaaactt ttggatgttc ggtttattct ttttctttta cttttttatc
            atgggagcct acttcccgtt tttcccgatt tggctacatg acatcaacca
            tatcagcaaa agtgatacgg gtattatttt tgccgctatt tctctgttct
            cgctattatt ccaaccgctg tttggtctgc tttctgacaa actcgggctg
            cgcaaatacc tgctgtggat tattaccggc atgttagtga tgtttgcgcc
            gttctttatt tttatcttcg ggccactgtt acaatacaac attttagtag
            gatcgattgt tggtggtatt tatctaggct tttgttttaa cgccggtgcg
            ccagcagtag aggcatttat tgagaaagtc agccgtcgca gtaatttcga
            atttggtcgc gcgcggatgt ttggctgtgt tggctgggcg ctgtgtgcct
            cgattgtcgg catcatgttc accatcaata atcagtttgt tttctggctg
            ggctctggct gtgcactcat cctcgccgtt ttactctttt tcgccaaaac
            ggatgcgccc tcttctgcca cggttgccaa tgcggtaggt gccaaccatt
            cggcatttag ccttaagctg gcactggaac tgttcagaca gccaaaactg
            tggtttttgt cactgtatgt tattggcgtt tcctgcacct acgatgtttt
            tgaccaacag tttgctaatt tctttacttc gttctttgct accggtgaac
            agggtacgcg ggtatttggc tacgtaacga caatgggcga attacttaac
            gcctcgatta tgttctttgc gccactgatc attaatcgca tcggtgggaa
            aaacgccctg ctgctggctg gcactattat gtctgtacgt attattggct
            catcgttcgc cacctcagcg ctggaagtgg ttattctgaa aacgctgcat
            atgtttgaag taccgttcct gctggtgggc tgctttaaat atattaccag
            ccagtttgaa gtgcgttttt cagcgacgat ttatctggtc tgtttctgct
            tctttaagca actggcgatg atttttatgt ctgtactggc gggcaatatg
            tatgaaagca tcggtttcca gggcgcttat ctggtgctgg gtctggtggc
            gctgggcttc accttaattt ccgtgttcac gcttagcggc cccggcccgc
            tttccctgct gcgtcgtcag gtgaatgaag tcgcttaa"""

LacY_seq = Sequence('Lac_seq', sequence2, SBOL_ENCODING_IUPAC)
doc.addSequence(LacY_seq)

#Composition
composition_component = doc.componentDefinitions.create("composition_component")
composition_component.assemblePrimaryStructure([GFP, LacY])
for cd in composition_component.getPrimaryStructure():
    print(cd.displayId)
    
nucleotides = composition_component.compile()
# print (nucleotides)
# seq = composition_component.sequence
# print(seq.elements)

composition_component.roles = [SO_GENE]

#Export
doc.write('SBOL_example.xml')
