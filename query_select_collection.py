#this selects the first (5 in this case) items from the igem collection. Try pasting it into synbiohub.org/sparql
#should work as a basis for selecting and adding parts for the composite parts
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX sbh: <http://wiki.synbiohub.org/wiki/Terms/synbiohub#>
PREFIX prov: <http://www.w3.org/ns/prov#>
PREFIX sbol: <http://sbols.org/v2#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX purl: <http://purl.obolibrary.org/obo/>

SELECT
	?collect
	?comp
	?displayId
	?title
	?role
WHERE {
  	?collect sbol:member ?comp .
    filter (regex(?collect, library)) .
  	filter (regex(?role, 'http://identifiers.org/so/SO:')) .
	?comp sbol:role ?role .  
	?comp sbol:displayId ?displayId .
  	OPTIONAL {?comp dcterms:title ?title} .
  	#filter (regex(?displayId, '^((?!sequence).)*$')) . 
  }


OFFSET 0 LIMIT 5
