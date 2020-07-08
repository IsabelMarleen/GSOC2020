# Plugin-Submit-Test
A very simple submit plugin that returns sbol files with submit information

# Install
## Docker
Run `docker run --publish 8087:5000 --detach --name submit-plug synbiohub/plugin-submit-test:snapshot`
Check it is up using http://localhost:8087/status.

## Using Python
Run pip install -r requirements.txt to install the requirements. Then run FLASK_APP=app python -m flask run. A flask module will run at http://localhost:5000/.

# Testing
To create a test manifest use:

```run_manifest = {"manifest":[]}
for i in range(0,7):
  file_name = f'file_name{i}'
  file_type = f'file_type{i}'
  file_url = f'file_url{i}'
  run_manifest['manifest'].append({"url":file_url, "filename":file_name, "edam":file_type})
```
