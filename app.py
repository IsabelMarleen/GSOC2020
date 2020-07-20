from flask import Flask, request, abort, send_file, jsonify
import os, shutil, glob, random, string
from Excel import read_library
from sbol2 import *
#import all functions from .py files

app = Flask(__name__)

@app.route("/status")
def status():
    return("The Submit Test Plugin Flask Server is up and running")



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
        useful_types = {'application/xml'}
        
        file_type_acceptable = file_type in acceptable_types
        file_type_useable = file_type in useful_types
        
        #to ensure all file types are accepted
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
    #file_path = os.path.join(cwd, "Test.xml")
    
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
            #Create own xml files using Excel.py etc.
            with open(file_path, 'r') as xmlfile:
                result = xmlfile.read()
            
            # #create random string of letters that is 15 long for display_id
            # length = 15
            # letters = string.ascii_lowercase
            # result_str = ''.join(random.choice(letters) for i in range(length))
            # display_id = result_str
                    
            # #put in the url, filename, and instance given by synbiohub
            # result = result.replace("TEST_FILE", file_name)
            # result = result.replace("REPLACE_DISPLAYID", display_id)
            # result = result.replace("REPLACE_FILENAME", file_name)
            # result = result.replace("REPLACE_FILETYPE", file_type)
            # result = result.replace("REPLACE_FILEURL", file_url)
            # result = result.replace("FILE_DATA_REPLACE", data)
            # result = result.replace("DATA_REPLACE", str(run_manifest))
            
            start_row = 13
            nrows = 8
            description_row = 9
            description_col = [0]
            use_cols = [0,1]
            
            filled_library, filled_library_metadata, filled_description = read_library(path_filled,  
                            start_row = start_row, nrows = nrows, description_row = description_row)
            # blank_library, blank_library_metadata, blank_description = read_library(path_blank,  
            #                 start_row = start_row, nrows = nrows, description_row = description_row)
            
            
            ontology = pd.read_excel(path_filled, header=None, sheet_name= "Ontology Terms", skiprows=3, index_col=0)
            ontology= ontology.to_dict("dict")[1]
            
            
            #Quality control spreadsheet
            
            #Description
            if filled_description.columns != "Design Description":
                col = col_to_excel(description_col+1)
                logging.warning(f"{col}{description_row+1} has been corrupted, it should be labelled 'Design Description' with the description in A11")
            
            #Metadata
            # comparison = np.where((filled_library_metadata == blank_library_metadata)|(blank_library_metadata.isna()), True, False)
            # excel_cell_names = []
            # for column in range(0, len(use_cols)):
            #     for row in range(0, comparison.shape[0]):
            #         col = use_cols[column]
            #         excel_cell_names.append(f"{col_to_excel(col+1)}{row+1}")
            # excel_cell_names = np.reshape(excel_cell_names, comparison.shape, order='F')
            # excel_cell_names = pd.DataFrame(excel_cell_names)
            # excel_cell_names.where(np.logical_not(comparison))
            
            # if not(comparison.all()) :
            #     logging.warning("Some cells do not match the template")
            #     for number in range(0, nrows-1) :
            #         if filled_library_metadata.iloc[number, 0] != blank_library_metadata.iloc[number, 0]:
            #             logging.warning(f"""The excel cell {excel_cell_names.loc[number, 0]} has been corrupted and 
            #                   should contain {blank_library_metadata.iloc[number, 0]}""")
                              
            #Library data
            # filled_columns = set(filled_library.columns)
            # blank_columns = set(blank_library.columns)
            
            # if not(blank_columns.issubset(filled_columns)) :
            #     missing_columns = blank_columns - filled_columns
            #     logging.warning(f"Some of the required columns are missing. They are {missing_columns}.")
            
            
            #Create SBOL document
            doc = Document()
            Config.setOption('sbol_typed_uris', False)
            
            #Define SBOL object and components
            #Parts Library
            molecule_type = BIOPAX_DNA #Change later
            part_column = "Part Name"
            sequence_column = "Sequence"
            description_column = "Description (Optional)"
            role_column = "Role"
            length_column = "length (bp)"
            
            for index, row in filled_library.iterrows():
                component = ComponentDefinition(row[part_column], molecule_type)
                component.roles = ontology[row[role_column]]
                component.name = row[part_column]
                if not(pd.isnull(row[description_column])):
                    component.description = row[description_column]
                doc.addComponentDefinition(component)
                
                row[sequence_column] = "".join(row[sequence_column].split())
                row[sequence_column] = row[sequence_column].replace( u"\ufeff", "")
                row[sequence_column] = row[sequence_column].lower()
                if len(row[sequence_column]) != row[length_column]:
                    logging.warning(f"The length of the sequence {row[part_column]} does not coincide with the length in the corresponding column 'length (bp)'")
                sequence = Sequence(f"{row[part_column]}_sequence", row[sequence_column], SBOL_ENCODING_IUPAC)
                doc.addSequence(sequence)
                component.sequences = sequence
            
            #Metadata
            doc.description = str(filled_description.values)
            doc.name = filled_library_metadata.iloc[0, 1]
            
            doc.write('result.xml')

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
