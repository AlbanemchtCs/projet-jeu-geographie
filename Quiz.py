# -*- coding: utf-8 -*-
"""
Created on Thu Dec 22 17:26:18 2022

@author: Admin
"""
from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd
import json
from sparQL_query import import_neighbors_dataframe,import_countries_dataframe, result_query
from difflib import SequenceMatcher, get_close_matches
import random

DATAFRAME_COUNTRIES = import_countries_dataframe()
POINT_NEIGHBOR = 1
POINT_QUESTION = 2
THRESHOLD_SIMILARITY = 0.7

"""
Quiz : Object used to generate questions and process the answers
init_country : french name of the initiale country
corpus : Dictionnary of questions (check the example in sparQL_query.py)
"""
class Quiz():
    def __init__(self,init_country = None,corpus = {}):
        if(init_country is None):
            sample = DATAFRAME_COUNTRIES.sample()
            self.current_country_name = sample.iloc[0]['country_name']
            self.current_country_id = sample.index[0]
        else:
            self.current_country_name = init_country
            self.current_country_id = DATAFRAME_COUNTRIES[DATAFRAME_COUNTRIES['country_name'] == init_country].index[0]
        self.points = 0
        
        self.corpus = corpus
        self.validated_countries = []
        self.lost = False
        self.potential_question = set(range(len(self.corpus)))
    """
    next_country : protocole to select a new country
    """
    def next_country(self):
        
        
        #Ask current country's neighbors
        neighbors = import_neighbors_dataframe(self.current_country_id)
        if(len(neighbors)>0):
            neighbors_kept = neighbors[~neighbors['country_name'].isin(self.validated_countries)]
        else:
            neighbors_kept = neighbors
        # If there isn't other neighbor the quiz select a new random country
        if(len(neighbors_kept) == 0):
            sample = DATAFRAME_COUNTRIES[~DATAFRAME_COUNTRIES['country_name'].isin(self.validated_countries)].sample()
            self.current_country_id = sample.index[0]
            self.current_country_name = sample.iloc[0]['country_name']
            print('Il y a pas de voisin potentiel, vous êtes téléporté vers '+ self.current_country_name+'.... ')
            return None
        else:
            retry = True
            while(retry):
                retry = False
                # user type a neighbor country or not
                answer = input(f'Donnez un pays voisin de {self.current_country_name} : ')
                # Compute distances between answer and potential neighbor names
                neighbors_list = list(neighbors['country_name'])
                match = get_close_matches(answer,neighbors_list,cutoff = THRESHOLD_SIMILARITY)
                
                # Case where answer is validated
                if(len(match)>0):
                    #  but already used, the user has a new chance
                    if(match[0] in self.validated_countries):
                       print('Oui mais non... Vous avez déjà parcouru '+ match[0] + '. Réessayez...')
                       retry = True 
                    # Case where answer is accepted
                    else:
                        #Add the last country
                        self.points += POINT_NEIGHBOR
                        print('Bravo! ' + match[0] + ' est bien un voisin de ' + self.current_country_name)
                        self.current_country_id = neighbors.index[neighbors_list.index(match[0])]
                        self.current_country_name = match[0]
                        self.potential_question = set(range(len(self.corpus)))
                        return True
                # Case where answer is wrong
                else:
                    self.lost = True
                    print('FAUX! Les voisins non parcourus étaient les suivants : ')
                    print( *list(neighbors_kept['country_name']), sep=', ')
                    return False
    """
    next_question : protocole to ask a new question about the current country
    """
    def next_question(self):
        finding_question = True
        results = None
        # Iterate until a valid question is found
        while(finding_question and len(self.potential_question) > 0):
            sample = random.sample(self.potential_question,1)[0]
            results = result_query(self.corpus[sample]['query'],self.current_country_id)
            if(not results is None):
                finding_question = False
            self.potential_question.remove(sample)
        # Case where no question is found
        if(results is None):
            print(f"Je n'ai pas de question pour {self.current_country_name}")
            return None
        # Case where a question is found
        else:
            # Ask a question about the current country
            answer = input(self.corpus[sample]['question'].format(self.current_country_name)+ ' : ')
            # Numerical case
            if(self.corpus[sample]['answer_type'] in [int,float]):
                # Answer is valid
                convert = True
                try: 
                    float(answer)
                except ValueError : convert = False
                if(convert and abs(float(answer)-float(results[0])) <= float(results[0])*self.corpus[sample]['error_ratio']):
                    self.points = POINT_QUESTION
                    print("Bonne réponse ! La réponse exacte était " + results[0] )
                    if(not self.current_country_name in self.validated_countries):
                        self.validated_countries += [self.current_country_name]
                    return True
                # Answer is wrong
                else:
                    self.lost = True
                    print("Mauvaise réponse... La réponse exacte était " + results[0])
                    return False
            # String case
            elif(self.corpus[sample]['answer_type'] is str):
                match = get_close_matches(answer,results,cutoff = THRESHOLD_SIMILARITY)
                # Answer is valid
                if(len(match) >= 1 ):
                    print("Bonne réponse ! c'était bien " + match[0])
                    if(not self.current_country_name in self.validated_countries):
                        self.validated_countries += [self.current_country_name]
                    return True
                # Answer is wrong
                else:
                    self.lost = True
                    print("Mauvaise réponse... c'était " + ', '.join(results))
                    return False
                
                