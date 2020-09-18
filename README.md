# GSoC2020

This repository represents the raw state and tracked the progress of my Google Summer of Code 2020 project. If you are interested in the tidy version that is continously being developed and intended to be used, you should look at the following repositories. The project was split into three repositories, one for each of the plugins that were developed in the context of this project and one for the functionality of converting Excel into SBOL itself.

- Plugin Submit Excel Library (https://github.com/SynBioHub/Plugin-Submit-Excel-Library)
- Plugin Submit Excel Library (https://github.com/SynBioHub/Plugin-Submit-Excel-Composition)
- Excel to SBOL (https://github.com/SynBioDex/Excel-to-SBOL)

My progress throughout the summer can also be understodd by looking at the blog I kept for that purpose (https://medium.com/@IsaMarleen).

## Spreadsheet Plug-in for SynBioHub

Synthetic Biology is a discipline that connects many disciplines and heterogeneous researchers.
To be useful as a tool, a platform such as SynBioHub should reflect this diversity. SynBioHub is
a repository of genetic components and designs and can represent a powerful way to share and
curate synthetic biology projects. To do so, it should invite and fulfill the needs of
bioinformaticians and mathematicians while at the same time bridging the gap to wet lab
experimentalists. One of these differences is the common preference of wet lab biologists to use
spreadsheets, which as of now cannot be used as input for SynBioHub. This can be changed by
creating a plugin, which accepts a spreadsheet as input and converts it into SBOL which can be
processed by SynBioHub. This could simplify the process of data curation for publication by
bridging the gap between those that perform the experiments and those that write about them
from the very beginning.
