from flask import Flask, request, abort, send_file, jsonify
import os, shutil, glob

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
        file_type = file['edam']
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
    
    run_manifest = request.get_json(force=True)
    
    #run_manifest = request.json['manifest']['files']
    files = run_manifest['manifest']['files']
    
    cwd = os.getcwd()
    file_path = os.path.join(cwd, "Test.xml")
    run_response_manifest = {"results":[]}
    
    #files = data['manifest']['files']
    
    for file in files:
        try:
            file_name = file['filename']
            file_type = file['edam']
            file_url = file['url']
            data = str(file)
           
            converted_file_name = f"{file_name}.converted"
            file_path_out = os.path.join(cwd, "To_zip", converted_file_name)
        
            ########## REPLACE THIS SECTION WITH OWN RUN CODE #################
            with open(file_path, 'r') as xmlfile:
                result = xmlfile.read()
                            
            #put in the url, filename, and instance given by synbiohub
            result = result.replace("TEST_FILE", file_name)
            result = result.replace("REPLACE_FILENAME", file_name)
            result = result.replace("REPLACE_FILETYPE", file_type)
            result = result.replace("REPLACE_FILEURL", file_url)
            result = result.replace("FILE_DATA_REPLACE", data)
            result = result.replace("DATA_REPLACE", str(run_manifest))
            ################## END SECTION ####################################
            
            # with open(file_path_out, 'w') as xmlfile:
            #     xmlfile.write(result)
            
            #add name of converted file to manifest
            # run_response_manifest["results"].append({"filename":converted_file_name,
            #                             "sources":[file_name]})
            file_list = glob.glob(os.path.join(cwd, '*'))
            return_str = str(cwd)+", "+str(file_list)
            return (return_str)
        except Exception as e:
            print(e)
            abort(415)
            
    # #create manifest file
    # file_path_out = os.path.join(cwd, "To_zip", "manifest.json")
    # with open(file_path_out, 'w') as manifest_file:
    #         manifest_file.write(str(run_response_manifest)) 
        
    # #create zip file of converted files and manifest
    # zip_path_in = os.path.join(cwd, "To_zip")
    # zip_path_out = os.path.join(cwd, "Zip")
    # shutil.make_archive(zip_path_out, 'zip', zip_path_in)
    
    # #clear To_zip directory
    # shutil.rmtree(zip_path_in)
    # os.makedirs(zip_path_in)
    
    # return send_file(f"{zip_path_out}.zip")
    
    # os.remove(f"{zip_path_out}.zip")
