# GSoC2020

This repository has been archived, because it tracked the progress of my Google Summer of Code 2020 project and is no longer being maintained. The resulting software that is continously being developed and intended for use can be found in the following two repositories. The project was split into two repositories, one for the SynBioHub plugins that were developed in the context of this project and one for the Python package for converting Excel into SBOL itself.

- [Excel SynBioHub Submission Plugin](https://github.com/SynBioHub/Plugin-Submit-Excel2SBOL)
- [Excel to SBOL package](https://github.com/SynBioDex/Excel-to-SBOL)

My progress throughout the summer can also be understood by looking at the blog I kept for that purpose (https://medium.com/@IsaMarleen).

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
