# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 14:54:07 2020

@author: JVM
"""

import os, shutil
from flask import request

cwd = os.getcwd()

run_manifest = {"manifest":[]}
for i in range(0,7):
    file_name = f'file_name{i}'
    file_type = f'file_type{i}'
    file_url = f'file_url{i}'
    run_manifest['manifest'].append({"url":file_url,
                                     "filename":file_name,
                                     "edam":file_type})


#run_manifest = request.json['manifest']['files']
files = run_manifest['manifest']
file_path = os.path.join(cwd, "Test.xml")
run_response_manifest = {"results":[]}

for file in files:
    file_name = file['filename']
    file_type = file['edam']
    file_url = file['url']
    data = str(file)
   
    converted_file_name = f"{file_name}.converted"
    file_path_out = os.path.join(cwd, "To_zip", converted_file_name )

    
    with open(file_path, 'r') as xmlfile:
        result = xmlfile.read()
                    
    #put in the url, filename, and instance given by synbiohub
    result = result.replace("TEST_FILE", file_name)
    result = result.replace("REPLACE_FILENAME", file_name)
    result = result.replace("REPLACE_FILETYPE", file_type)
    result = result.replace("REPLACE_FILEURL", file_url)
    result = result.replace("FILE_DATA_REPLACE", str(data))
    result = result.replace("DATA_REPLACE", str(run_manifest))
    
    with open(file_path_out, 'w') as xmlfile:
        xmlfile.write(result)
    
    #add name of converted file to manifest
    run_response_manifest["results"].append({"filename":converted_file_name,
                                "sources":[file_name]})

#create manifest file
file_path_out = os.path.join(cwd, "To_zip", "manifest.json")
with open(file_path_out, 'w') as manifest_file:
        manifest_file.write(str(run_response_manifest)) 
    
#create zip file of converted files and manifest
zip_path_in = os.path.join(cwd, "To_zip")
zip_path_out = os.path.join(cwd, "Zip")
shutil.make_archive(zip_path_out, 'zip', zip_path_in)

#clear To_zip directory
shutil.rmtree(zip_path_in)
os.makedirs(zip_path_in)