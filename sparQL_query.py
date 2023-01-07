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
    query_countries = """
    SELECT ?country ?countryLabel ?nb
    WHERE{
        {
    SELECT DISTINCT ?country (COUNT(?neighbor) as ?nb)
    WHERE
    {
     
     ?country wdt:P31 wd:Q3624078.
     ?country wdt:P47 ?neighbor.
     ?neighbor wdt:P31 wd:Q3624078.
     #not a former country
     FILTER NOT EXISTS {?country wdt:P31 wd:Q3024240}
     #and no an ancient civilisation (needed to exclude ancient Egypt)
     FILTER NOT EXISTS {?country wdt:P31 wd:Q28171280}
     
     }
    GROUP BY ?country
    }
    SERVICE wikibase:label { bd:serviceParam wikibase:language "fr" }
    }
    
    """
    sparql.setQuery(query_countries)
    
    result= sparql.queryAndConvert()['results']['bindings']
    data = pd.DataFrame([{"id" : elem['country']['value'].split('/')[-1],"country_name" : elem['countryLabel']['value'],"neighbor" : int(elem['nb']['value'].split('/')[-1])} for elem in result]).drop(0).set_index('id')
    return data

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
        return [r[list(result[0].keys())[0]]['value'] for r in result]


Question_corpus = {0 : {'question' : "Combien il y a t-il t'habitant en/au {}? (+/-10%)",
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
                            """SELECT DISTINCT ?capitalLabel 
                            WHERE {{
                                wd:{} wdt:P36 ?capital.
                                SERVICE wikibase:label {{ bd:serviceParam wikibase:language "fr" }}
                                }}
                            """},
                    2: {'question' : "Quelle est la monnaie utilisé en {}?",
                        'answer_type' : str,
                        'query':
                            """SELECT DISTINCT ?currencyLabel 
                            WHERE {{
                                wd:{} wdt:P38 ?currency.
                                SERVICE wikibase:label {{ bd:serviceParam wikibase:language "fr" }}
                                }}
                            """},
                    3: {'question' : "Les voitures roulent à gauche ou à droite en {}?",
                        'answer_type' : str,
                        'query':
                            """SELECT DISTINCT ?currencyLabel 
                            WHERE {{
                                wd:{} wdt:P1622 ?currency.
                                SERVICE wikibase:label {{ bd:serviceParam wikibase:language "fr" }}
                                }}
                            """},
                    4: {'question' : "Quelle est la langue officielle en {}?",
                        'answer_type' : str,
                        'query':
                            """SELECT DISTINCT ?languageLabel 
                            WHERE {{
                                wd:{} wdt:P37 ?language.
                                SERVICE wikibase:label {{ bd:serviceParam wikibase:language "fr" }}
                                }}
                            """},
                    5: {'question' : "Qui est le chef de l'état de {}?",
                        'answer_type' : str,
                        'query':
                            """SELECT DISTINCT ?titreLabel 
                            WHERE {{
                                wd:{} wdt:P35 ?titre.
                                SERVICE wikibase:label {{ bd:serviceParam wikibase:language "fr" }}
                                }}
                            """},
                    6: {'question' : "Quel est le continent de {}?",
                        'answer_type' : str,
                        'query':
                            """SELECT DISTINCT ?continentLabel 
                            WHERE {{
                                wd:{} wdt:P30 ?continent.
                                SERVICE wikibase:label {{ bd:serviceParam wikibase:language "fr" }}
                                }}
                            """},
                    7: {'question' : "Quel régime politique de {}?",
                        'answer_type' : str,
                        'query':
                            """SELECT DISTINCT ?regimeLabel 
                            WHERE {{
                                wd:{} wdt:P122 ?regime.
                                SERVICE wikibase:label {{ bd:serviceParam wikibase:language "fr" }}
                                }}
                            """},
                    8: {'question' : "Quel est l'âge de la majorité en {}?",
                        'answer_type' : int,
                        'error_ratio' : 0,
                        'query':
                            """SELECT DISTINCT ?age 
                            WHERE {{
                                wd:{} wdt:P2997 ?age.
                                SERVICE wikibase:label {{ bd:serviceParam wikibase:language "fr" }}
                                }}
                            """}
                        
                        }

                   