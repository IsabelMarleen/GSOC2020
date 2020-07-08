# Plugin-Submit-Test
A very simple submit plugin that returns sbol files with submit information

# Install
## Docker
Run `docker run --publish 8087:5000 --detach --name submit-plug synbiohub/plugin-submit-test:snapshot`
Check it is up using localhost:8087.

## Using Python
Run pip install -r requirements.txt to install the requirements. Then run FLASK_APP=app python -m flask run. A flask module will run at localhost:5000/.
