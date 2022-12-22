# -*- coding: utf-8 -*-
"""
Created on Wed Dec 21 22:09:18 2022

@author: Admin
"""

from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd
import json 


sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
sparql.setReturnFormat(JSON)

"""
import_countries_dataframe : get IDs and names of all valid countries
"""
def import_countries_dataframe():
    query_countries = """SELECT DISTINCT ?countryLabel ?country
    WHERE
    {
     ?country wdt:P31 wd:Q3624078.
     #not a former country
     FILTER NOT EXISTS {?country wdt:P31 wd:Q3024240}
     #and no an ancient civilisation (needed to exclude ancient Egypt)
     FILTER NOT EXISTS {?country wdt:P31 wd:Q28171280}
     
     SERVICE wikibase:label { bd:serviceParam wikibase:language "fr" }
     }
    ORDER BY ?countryLabel"""
    sparql.setQuery(query_countries)
    
    result= sparql.queryAndConvert()['results']['bindings']
    return pd.DataFrame([{"id" : elem['country']['value'].split('/')[-1],"country_name" : elem['countryLabel']['value']} for elem in result]).drop(0).set_index('id')

"""
import_neighbors_dataframe : get IDs and names of all neighbor countries
     country_id : ID of the country
"""
def import_neighbors_dataframe(country_id):
    query_neighbors = f"""SELECT DISTINCT ?neighborsLabel ?neighbors
    WHERE
    {{
      ?neighbors wdt:P31 wd:Q3624078.
      ?neighbors wdt:P47 wd:{country_id}.
      #not a former country
      FILTER NOT EXISTS {{?neighbors wdt:P31 wd:Q3024240}}
      #and no an ancient civilisation (needed to exclude ancient Egypt)
      FILTER NOT EXISTS {{?neighbors wdt:P31 wd:Q28171280}}

      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "fr" }}
    }}
    ORDER BY ?neighborsLabel"""
    sparql.setQuery(query_neighbors)
    result = sparql.queryAndConvert()['results']['bindings']
    Neighbors = pd.DataFrame([{"id" : elem['neighbors']['value'].split('/')[-1],"country_name" : elem['neighborsLabel']['value']} for elem in result])
    if(len(Neighbors) != 0):
        Neighbors = Neighbors.set_index('id')
    return Neighbors

"""
result_query : protocole to get answer from wikidata
"""
def result_query(query,country_id):
    sparql.setQuery(query.format(country_id))
    result = sparql.queryAndConvert()['results']['bindings']
    if(result == []):
        return None
    else:
        return result[0][list(result[0].keys())[0]]['value']


Question_corpus = {0 : {'question' : "Combien il y a t-il t'habitant en/au {}?",
                        'answer_type' : int,
                        'error_ratio' : 0.1,
                        'query' : 
                            """SELECT DISTINCT ?population 
                            WHERE {{
                                wd:{} wdt:P1082 ?population.
                                SERVICE wikibase:label {{ bd:serviceParam wikibase:language "fr" }}
                                }}
                            """},
                   1 : {'question' : "Quelle est la capitale de {}?",
                        'answer_type' : str,
                        'query' : 
                            """SELECT DISTINCT ?xLabel 
                            WHERE {{
                                wd:{} wdt:P36 ?x.
                                SERVICE wikibase:label {{ bd:serviceParam wikibase:language "fr" }}
                                }}
                            """}
                        
                        }

                   