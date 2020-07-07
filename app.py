from flask import Flask, request, abort, jsonify
import os

app = Flask(__name__)

@app.route("/status")
def status():
    return("The Visualisation Test Plugin Flask Server is up and running")

@app.route("/evaluate", methods=["POST", "GET"])
def evaluate():
    return("The type sent is an accepted type")

@app.route("/run", methods=["POST"])
def run():
    data = request.get_json(force=True)
    
    files = data['manifest']['files']

    
    cwd = os.getcwd()
    file_path = os.path.join(cwd, "Test.xml")
    
    for file in files:
        try:
            file_url = file['url']
            file_name = file['filename']
            file_type = file['type']
            
            with open(file_path, 'r') as xmlfile:
                result = xmlfile.read()
                
            #put in the url, filename, and instance given by synbiohub
            result = result.replace("TEST_FILE", file_name)
            result = result.replace("REPLACE_FILENAME", file_name)
            result = result.replace("REPLACE_FILETYPE", file_type)
            result = result.replace("REPLACE_FILEURL", file_url)
            
            result = result.replace("REQUEST_REPLACE", str(data))
                
            return result
        except Exception as e:
            print(e)
            abort(404)