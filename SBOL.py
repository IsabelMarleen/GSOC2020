#Setup
import sbol
from sbol import Document
from sbol import *

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