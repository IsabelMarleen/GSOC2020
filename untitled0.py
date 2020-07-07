# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 14:54:07 2020

@author: JVM
"""

import os
import shutil

cwd = os.getcwd()
file_path = os.path.join(cwd, "Test.xml")

for i in range(0,7):

    file_name = f'file_name{i}'
    file_type = f'file_type{i}'
    file_url = f'file_url{i}'
    data = f'data{i}'
    
    file_path_out = os.path.join(cwd, "To_zip", f"{file_name}.xml")

    
    with open(file_path, 'r') as xmlfile:
        result = xmlfile.read()
                    
    #put in the url, filename, and instance given by synbiohub
    result = result.replace("TEST_FILE", file_name)
    result = result.replace("REPLACE_FILENAME", file_name)
    result = result.replace("REPLACE_FILETYPE", file_type)
    result = result.replace("REPLACE_FILEURL", file_url)
    
    result = result.replace("DATA_REPLACE", str(data))
    
    with open(file_path_out, 'w') as xmlfile:
        xmlfile.write(result)
        
zip_path_in = os.path.join(cwd, "To_zip")
zip_path_out = os.path.join(cwd, "Zip")
shutil.make_archive(zip_path_out, 'zip', zip_path_in)


shutil.rmtree(zip_path_in)
os.makedirs(zip_path_in)