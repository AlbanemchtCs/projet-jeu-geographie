# -*- coding: utf-8 -*-
"""
Created on Thu Dec 22 17:26:18 2022

@author: Admin
"""
from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd
import json
from sparQL_query import import_neighbors_dataframe,import_countries_dataframe, result_query
from difflib import SequenceMatcher
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
    def __init__(self,init_country,corpus = {}):
        self.points = 0
        self.current_country_name = init_country
        self.current_country_id = DATAFRAME_COUNTRIES[DATAFRAME_COUNTRIES['country_name'] == init_country].index[0]
        self.corpus = corpus
        self.validated_countries = []
        self.lost = False
        self.potential_question = set(range(len(self.corpus)))
    """
    next_country : protocole to select a new country
    """
    def next_country(self):
        #Add the last country
        self.validated_countries += [self.current_country_name]
        
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
        else:
            retry = True
            while(retry):
                retry = False
                # user type a neighbor country or not
                answer = input(f'Donnez un pays voisin de {self.current_country_name} : ')
                i_max = 0
                ratio = 0
                # Compute distances between answer and potential neighbor names
                for i in range(len(neighbors)):
                    cal_ratio = SequenceMatcher(None,answer,neighbors.iloc[i]['country_name']).ratio()
                    if(ratio < cal_ratio):
                        ratio = cal_ratio
                        i_max = i
                # Case where answer is validated but already yet, the user has a new chance
                if(ratio >= THRESHOLD_SIMILARITY and neighbors.iloc[i_max]['country_name'] in self.validated_countries):
                    print('Oui mais non... Vous avez déjà parcouru '+ neighbors.iloc[i_max]['country_name'] + '. Réessayez...')
                    retry = True
                # Case where answer is accepted
                elif(ratio >= THRESHOLD_SIMILARITY):
                    self.points += POINT_NEIGHBOR
                    print('Bravo! ' + neighbors.iloc[i_max]['country_name'] + ' est bien un voisin de ' + self.current_country_name)
                    self.current_country_id = neighbors.index[i_max]
                    self.current_country_name = neighbors.iloc[i_max]['country_name']
                    self.potential_question = set(range(len(self.corpus)))
                # Case where answer is wrong
                else:
                    self.lost = True
                    print('FAUX! Les voisins non parcourus étaient les suivants : ')
                    print( *list(neighbors['country_name']), sep=', ')
        return self.lost
    """
    next_question : protocole to ask a new question about the current country
    """
    def next_question(self):
        finding_question = True
        result = None
        # Iterate until a valid question is found
        while(finding_question and len(self.potential_question) > 0):
            sample = random.sample(self.potential_question,1)[0]
            result = result_query(self.corpus[sample]['query'],self.current_country_id)
            if(not result is None):
                finding_question = False
            self.potential_question.remove(sample)
        # Case where no question is found
        if(result is None):
            print(f"Je n'ai pas de question pour {self.current_country_name}")
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
                if(convert and abs(float(answer)-float(result)) <= float(result)*self.corpus[sample]['error_ratio']):
                    self.points = POINT_QUESTION
                    print("Bonne réponse ! La réponse exacte était " + result )
                # Answer is wrong
                else:
                    self.lost = True
                    print("Mauvaise réponse... La réponse exacte était " + result)
            # String case
            elif(self.corpus[sample]['answer_type'] is str):
                # Answer is valid
                if(SequenceMatcher(None,answer,result).ratio() >= THRESHOLD_SIMILARITY ):
                    print("Bonne réponse ! c'était bien " + result )
                # Answer is wrong
                else:
                    self.lost = True
                    print("Mauvaise réponse... c'était " + result)
        return self.lost
                
                