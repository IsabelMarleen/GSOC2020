from flask import Flask, request, abort, send_file, jsonify
import os, shutil, glob, random, string

app = Flask(__name__)

@app.route("/status")
def status():
    return("The Submit Test Plugin Flask Server is up and running")



@app.route("/evaluate", methods=["POST"])
def evaluate():
    #uses edam ontology: http://edamontology.org/page
    #https://bioportal.bioontology.org/ontologies/EDAM?p=classes
    
    eval_manifest = request.get_json(force=True)
    files = eval_manifest['manifest']['files']
    
    eval_response_manifest = {"manifest":[]}
    
    for file in files:
        file_name = file['filename']
        file_type = file['type']
        file_url = file['url']
        
        ########## REPLACE THIS SECTION WITH OWN RUN CODE #################
        acceptable_types = {'http://edamontology.org/format_3468',
                            'http://edamontology.org/format_3620'}
        
        #could change what appears in the useful_types based on the file content
        useful_types = {'http://edamontology.org/format_3752'}
        
        file_type_acceptable = file_type in acceptable_types
        file_type_useable = file_type in useful_types
        
        #to enseure all file types are accepted
        file_type_acceptable = True
        ################## END SECTION ####################################
        
        if file_type_acceptable:
            useableness = 2
        elif file_type_useable:
            useableness = 1
        else:
            useableness = 0
        
        eval_response_manifest["manifest"].append({
            "filename": file_name,
            "requirement": useableness})
       
    return jsonify(eval_response_manifest)


@app.route("/run", methods=["POST"])
def run():
    cwd = os.getcwd()
    
    zip_path_in = os.path.join(cwd, "To_zip")
    zip_path_out = os.path.join(cwd, "Zip")
    
    #make to zip directory
    os.makedirs(zip_path_in)
    
    #take in run manifest
    run_manifest = request.get_json(force=True)
    files = run_manifest['manifest']['files']
    
    #Remove this line if not needed
    file_path = os.path.join(cwd, "Test.xml")
    
    #initiate response manifest
    run_response_manifest = {"results":[]}
    
    
    for file in files:
        try:
            file_name = file['filename']
            file_type = file['type']
            file_url = file['url']
            data = str(file)
           
            converted_file_name = f"{file_name}.converted"
            file_path_out = os.path.join(zip_path_in, converted_file_name)
        
            ########## REPLACE THIS SECTION WITH OWN RUN CODE #################
            #read in Test.xml
            with open(file_path, 'r') as xmlfile:
                result = xmlfile.read()
            
            #create random string of letters that is 15 long for display_id
            length = 15
            letters = string.ascii_lowercase
            result_str = ''.join(random.choice(letters) for i in range(length))
            display_id = result_str
                    
            #put in the url, filename, and instance given by synbiohub
            result = result.replace("TEST_FILE", file_name)
            result = result.replace("REPLACE_DISPLAYID", display_id)
            result = result.replace("REPLACE_FILENAME", file_name)
            result = result.replace("REPLACE_FILETYPE", file_type)
            result = result.replace("REPLACE_FILEURL", file_url)
            result = result.replace("FILE_DATA_REPLACE", data)
            result = result.replace("DATA_REPLACE", str(run_manifest))
            ################## END SECTION ####################################
            
            #write out result to "To_zip" file
            with open(file_path_out, 'w') as xmlfile:
                xmlfile.write(result)
            
            # add name of converted file to manifest
            run_response_manifest["results"].append({"filename":converted_file_name,
                                        "sources":[file_name]})
            
        except Exception as e:
            print(e)
            abort(415)
            
    #create manifest file
    file_path_out = os.path.join(zip_path_in, "manifest.json")
    with open(file_path_out, 'w') as manifest_file:
            manifest_file.write(str(run_response_manifest)) 
        
    #create zip file of converted files and manifest
    shutil.make_archive(zip_path_out, 'zip', zip_path_in)
    
    #clear To_zip directory
    shutil.rmtree(zip_path_in)
    
    return send_file(f"{zip_path_out}.zip")
    
    #delete zip file
    os.remove(f"{zip_path_out}.zip")
