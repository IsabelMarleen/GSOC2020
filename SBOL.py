# -*- coding: utf-8 -*-


import sbol
from sbol import *
doc = Document()

setHomespace('http://sbols.org/CRISPR_Example')

cas9_generic = ComponentDefinition('cas9_generic', BIOPAX_PROTEIN)
doc.addComponentDefinition(cas9_generic)

cd0 = ComponentDefinition('cd0')

print(doc)