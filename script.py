# -*- coding: utf-8 -*-
"""
Created on Thu Dec 22 21:55:11 2022

@author: Admin
"""

from Quiz import Quiz
from sparQL_query import *
from utils import *
import sys
import os
import time
import random
import threading

"""
script.py : interface for the game
"""

"""
PREPARATION BEFORE PLAYING THE QUIZ
"""
# ------------------
# Introduction
# ------------------
os.system("cls" if os.name == "nt" else "clear")
print("-"*62,"🎲","-"*62) 
print_typing(f"{space('small')}Quiz Culture générale - Géographie\n") 
time.sleep(1.5)
print_typing("\nQuels sont les pays limitrophes de la France ? Quelle est la capitale de l'Uruguay ? Quelle est la majorité civile au Cameroun ?\n")
time.sleep(1.0)
print_typing("\nTestez vos connaissances en géographie en défiant votre famille ou vos amis !\n")
time.sleep(1.5)
print("""     
o               .        ___---___                    .                   
       .              .--\        --.     .     .         .
                    ./.;_.\     __/~ \.     
                   /;  / `-'  __\    . \                            
 .        .       / ,--'     / .   .;   \        |
                 | .|       /       __   |      -O-       .
                |__/    __ |  . ;   \ | . |      |
                |      /  \\_    . ;| \___|    
   .    o       |      \  .~\\___,--'     |           .
                 |     | . ; ~~~~\_    __|
    |             \    \   .  .  ; \  /_/   .
   -O-        .    \   /         . |  ~/                  .
    |    .          ~\ \   .      /  /~          o
  .                   ~--___ ; ___--~       
                 .          ---         .              -JT
""") 
time.sleep(1.5)
print("-"*127) 
time.sleep(1.5)

# ------------------
# Ready to start ?
# ------------------
# Asks the user if he is ready to play or not
ready_starting()

# ------------------
# Rules of the game
# ------------------
os.system("cls" if os.name == "nt" else "clear")
print("-"*62,"🚦","-"*62) 
print_typing(f"{space('very_large')}Règles du jeu\n") 
time.sleep(1.5)
print_typing("\nLe but du jeu est de parcourir le plus de pays possible. Pour avancer, chaque joueur commence son parcours dans un pays.\n")
time.sleep(1.5)
print_typing("\nQuestion 1. Le joueur doit dans un premier temps donner un pays limitrophe de l'endroit où il se trouve.\n")
time.sleep(1.5)
print_typing("\nQuestion 2. S'il réussit, il peut alors répondre à une question de culture générale sur le pays limitrophe.\n")
time.sleep(1.5)
print_typing("\nLa question 1 vaut un point, tandis que la question 2 vaut deux points. \nS'il ne réussit pas à répondre à la question 1, il devra attendre la prochaine manche.\n")
time.sleep(2)
print_typing("\nAstuce : réfléchissez-bien au pays limitrophe que vous choisissez, certains pays n'ont pas beaucoup de voisins !\n")
time.sleep(1.5)
print("-"*127) 
time.sleep(3)

# ------------------
# Preparation
# ------------------
os.system("cls" if os.name == "nt" else "clear")
print("-"*62,"📝","-"*62)
print_typing(f"{space('very_large')}Préparation \n")  
time.sleep(1.0)

# Number of rounds
rounds_nbr = rounds()

# Number and nicknames of players
nicknames_players = nicknames()

# Each player has their own quiz
Q = {j : Quiz(None,Question_corpus) for j in nicknames_players}

# Declaration of the list "countries_seen" for the countries that the player will have visited
countries_seen =[] 

"""
PLAYING THE QUIZ
"""
# ------------------
# Countdown timer
# ------------------
os.system("cls" if os.name == "nt" else "clear")
countdown(5)
time.sleep(1.5)

# ------------------
# Rounds
# ------------------
# Iteration of the questions for each round
for i in range(1, rounds_nbr +1):
    os.system("cls" if os.name == "nt" else "clear")
    print("-"*62,"▶️","-"*62) 
    print_typing(f"{space('large')}Manche numéro {i}\n") 
    print("-"*127) 
    time.sleep(2.5)

    # Iteration of the questions for every player
    for j in nicknames_players:
        os.system("cls" if os.name == "nt" else "clear")
        print_typing(f"\nJoueur {j}\n")
        time.sleep(1.5)
        print("-"*62,"❓","-"*62)
        print_typing(f"{space('very_large')}Question 1\n") 
        time.sleep(1.5)

        # If question 1 is correct, question 2 is asked
        if Q[j].next_country():
            time.sleep(2.5)
            os.system("cls" if os.name == "nt" else "clear")
            print(f"\nJoueur {j}")
            time.sleep(1)
            print("-"*62,"❓","-"*62)
            print_typing(f"{space('very_large')}Question 2\n") 
            time.sleep(1.5)
            Q[j].next_question()
            time.sleep(2.5)
        else: 
            time.sleep(1.5)

    # Result for every round
    os.system("cls" if os.name == "nt" else "clear")
    print("-"*62,"▶️","-"*62)
    print_typing(f"{space('medium')}Résultat Manche numéro {i}\n")
    print("-"*127) 
    time.sleep(2.5)
    print_typing('\n'.join([f'{j} : {Q[j].points}' for j in nicknames_players]))
    time.sleep(2)

"""
ENDING THE QUIZ
"""
# ------------------
# Final result
# ------------------
os.system("cls" if os.name == "nt" else "clear")
print("-"*62,"▶️","-"*62)
print_typing(f"{space('large')}Résultat Final\n")
print("-"*127) 
time.sleep(2.5)

# Displays the final scores and the final winner
final_result(nicknames_players, Q)

time.sleep(2.5)
os.system("cls" if os.name == "nt" else "clear")
