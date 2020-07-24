from flask import Flask, request, abort, send_file, jsonify
import os, shutil, glob, random, string
from Excel import read_library, quality_check, write_sbol
from sbol2 import *
#import all functions from .py files

app = Flask(__name__)

@app.route("/status")
def status():
    return("The Submit Excel Plugin Flask Server is up and running")



@app.route("/evaluate", methods=["POST"])
def evaluate():
    #uses MIME types
    #https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Common_types
    
    eval_manifest = request.get_json(force=True)
    files = eval_manifest['manifest']['files']
    
    eval_response_manifest = {"manifest":[]}
    
    for file in files:
        file_name = file['filename']
        file_type = file['type']
        file_url = file['url']
        
        ########## REPLACE THIS SECTION WITH OWN RUN CODE #################
        acceptable_types = {'application/vnd.ms-excel',
                            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'}
        
        #could change what appears in the useful_types based on the file content
        useful_types = {}
        
        file_type_acceptable = file_type in acceptable_types
        file_type_useable = file_type in useful_types
        ################## END SECTION ####################################
        
        if file_type_acceptable:
            useableness = 2
        # elif file_type_useable:
        #     useableness = 1
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
    
    #remove to zip directory if it exists
    try:
        shutil.rmtree(zip_path_in, ignore_errors=True)
    except:
        print("No To_zip exists currently")
        
    #make to zip directory
    os.makedirs(zip_path_in)
    
    #take in run manifest
    run_manifest = request.get_json(force=True)
    files = run_manifest['manifest']['files']
    
    #Remove this line if not needed
    file_path = os.path.join(cwd, "templates/darpa_template_blank.xlsx")
    
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
            #Create own xml files using Excel.py etc.            
            start_row = 13
            nrows = 8
            description_row = 9
            
            filled_library, filled_library_metadata, filled_description = read_library(file_url, 
                start_row = start_row, nrows = nrows, description_row = description_row)
            
            blank_library, blank_library_metadata, blank_description = read_library(file_path,  
                start_row = start_row, nrows = nrows, description_row = description_row)
            
            
            quality_check(filled_library, blank_library, filled_library_metadata, 
                          blank_library_metadata, filled_description, blank_description)
            
            
            doc = write_sbol(filled_library, filled_library_metadata, filled_description)
            
            doc.write(file_path_out)
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
    shutil.rmtree(zip_path_in, ignore_errors=True)
    
    return send_file(f"{zip_path_out}.zip")
    
    #delete zip file
    os.remove(f"{zip_path_out}.zip")
