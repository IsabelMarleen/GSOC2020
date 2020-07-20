# GSoC2020
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

https://medium.com/@IsaMarleen

# Plugin-Submit-Excel
A very simple submit plugin that returns sbol files with submit information

# Install
## Docker
Run `docker run --publish 8087:5000 --detach --name submit-plug synbiohub/plugin-submit-excel:snapshot`
Check it is up using http://localhost:8087/status.

## Using Python
Run pip install -r requirements.txt to install the requirements. Then run FLASK_APP=app python -m flask run. A flask module will run at http://localhost:5000/.

# Testing
To create a test manifest use (note that quotes must use " for postman):

```
run_manifest = {"manifest":[]}
for i in range(0,7):
  file_name = f'file_name{i}'
  file_type = f'file_type{i}'
  file_url = f'file_url{i}'
  run_manifest['manifest'].append({"url":file_url, "filename":file_name, "type":file_type})
```
Example manifest:
```
{"manifest": {"files":[
  {"url": "file_url0", "filename": "file_name0", "type": "file_type0"},
  {"url": "file_url1", "filename": "file_name1", "type": "file_type1"},
  {"url": "file_url2", "filename": "file_name2", "type": "file_type2"},
  {"url": "file_url3", "filename": "file_name3", "type": "file_type3"},
  {"url": "file_url4", "filename": "file_name4", "type": "file_type4"},
  {"url": "file_url5", "filename": "file_name5", "type": "file_type5"},
  {"url": "file_url6", "filename": "file_name6", "type": "file_type6"}]}}
  ```
