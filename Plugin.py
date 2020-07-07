#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 17:12:45 2020

@author: isapoetzsch
"""


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#FLASK_APP=app.py flask run
from flask import Flask, request, abort
#from Full_v004_20190506 import *
app = Flask(__name__)

#flask run --host=0.0.0.0
@app.route("/dnasubmit/status")
def imdoingfine():
    return("Not dead Jet")


@app.route("/dnasubmit/evaluate", methods=["POST"])
def evaluate():
    return("Accepting Everything")   #Only if it is an excel.xlsx accept it


@app.route("/dnasubmit/run", methods=["POST"])
def wrapper():
    data = request.json
    files = data['manifest']['files']

    for file in files:
        try:
            url = file['url']
            partname = file['filename']
            sbolcontent = DNA_to_GeneBank(url, partname) #function here, essentially Excel.py file
            return sbolcontent #sbol.xml file that is created
        except Exception as e:
            print(e)
            abort(404)