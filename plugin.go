#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 12:09:24 2020

@author: isapoetzsch
"""



from flask import Flask, request, abort
app = Flask(__name__)

#flask run --host=0.0.0.0
@app.route("/status")
def status():
    # This could be a more complicated check to see if dependencies are online

    return("online")

@app.route("/evaluate", methods=["POST", "GET"])
def evaluate():
    # This should examine request.body to see if a request can be handled
    package main

    import (
            "encoding/json"
            "fmt"
            "net/http"
    )
    
    func Evaluate(w http.ResponseWriter, r *http.Request) {
        // Decode JSON request from SynBioHub
        request := SubmitRequest{}
        err := json.NewDecoder(r.Body).Decode(&request)
        if err != nil {
            fmt.Fprintln(w, err.Error(), http.StatusInternalServerError)
            return
        }
    
        // Begin preparing response
        response := EvaluateResponse{}
    
        // We will respond to each file
        response.Files = make([]EvaluateFileResponse, len(request.Manifest))
        for i, file := range request.Manifest {
            responseFile := &response.Files[i]
            responseFile.Filename = file.Filename
    
            if (isFasta(file)) {
                responseFile.Requirement = WillHandle
            } else {
                responseFile.Requirement = WillNotUse
            }
        }
    
        // Write the response into JSON
        responseJson, err := JSONMarshal(response)
        if err != nil {
            fmt.Fprintln(w, err.Error(), http.StatusInternalServerError)
            return
        }
    
        // Send the JSON back to SynBioHub
        w.Write(responseJson)
    }
    
    func isFasta(file FileInfo) bool {
        // Fetch the file from the link provided by SynBioHub
        resp, err := http.Get(file.URL)
        if err != nil {
            fmt.Printf("Could not get file %s (%s). Assuming not FASTA.", file.Filename, file.URL)
            return false
        }
        defer resp.Body.Close()
    
        // Read the first byte, if it's equal to '>' assume it's a FASTA file
        buf := make([]byte, 1)
        n, err := resp.Body.Read(buf)
        if err != nil || n != 1 {
            fmt.Printf("Could not read file %s (%s). Assuming not FASTA.", file.Filename, file.URL)
            return false
        }
    
        firstChar := string(buf)
        return firstChar == ">" // not really a great FASTA check, but works
    }
    return("Allowed")


@app.route("/run", methods=["POST"])
def run():
    # This should return a result.

    return("")