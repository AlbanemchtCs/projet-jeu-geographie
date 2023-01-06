# -*- coding: utf-8 -*-
"""
Created on Thu Dec 22 21:55:11 2022

@author: Admin
"""

import os
import sys
import random
import time

"""
utils : python file containing all the useful functions for the script
"""

"""
print_typing : simulate typing
"""
def print_typing(str):
    for letter in str:
        sys.stdout.write(letter)
        sys.stdout.flush()
        time.sleep(0.01)

"""
countdown : countdown timer
"""
def countdown(t):
    while t > 0:
        time.sleep(0.5)
        print_typing(f"{t}")
        time.sleep(0.2)
        print_typing(".")
        time.sleep(0.2)
        print_typing(".")
        time.sleep(0.2)
        print_typing(".")
        t -= 1
    time.sleep(1.5)
    print_typing("C'est parti !\n")

"""
ready_starting : asks the user if he is ready to play, if not the program stops
"""
def ready_starting():
    # Asks the user if he is ready to play
    os.system("cls" if os.name == "nt" else "clear")
    userInput = input("\nÊtes-vous prêts à jouer [oui/non] ? ")

    while userInput not in ["oui","non"]:
        os.system("cls" if os.name == "nt" else "clear")
        time.sleep(1)
        print_typing("\nVeuillez choisir entre oui et non !\n")
        userInput = input("\nÊtes-vous prêts à jouer [oui/non] ? ")
        time.sleep(1)

    # If the answer is "non"
    if userInput != "oui":
        os.system("cls" if os.name == "nt" else "clear")
        time.sleep(1)
        print_typing("\nDommage, revenez une prochaine fois !\n")
        time.sleep(1)   
        exit()

"""
rounds : returns the number of rounds
"""
def rounds():
    # Choice of the number of rounds
    userInput = input("\nCombien de tour(s) voulez-vous jouer [1/2/3/4/5] ? ")

    while userInput not in ["1","2","3","4","5"]:
        os.system("cls" if os.name == "nt" else "clear")
        time.sleep(1)
        print_typing("\nVeuillez choisir un nombre compris entre 1 et 5 !\n")
        userInput = input("\nCombien de tour(s) voulez-vous jouer [1/2/3/4/5] ? ")
        time.sleep(1)

    rds_number = int(userInput)
    return rds_number

"""
nicknames : returns the number of players and their nicknames
"""
def nicknames():
    # Choice of the number of players
    os.system("cls" if os.name == "nt" else "clear")
    userInput = input("\nCombien de joueurs participent [2/3/4/5] ? ")
    
    while userInput not in ["2","3","4","5"]:
        os.system("cls" if os.name == "nt" else "clear")
        time.sleep(1)
        print_typing("\nVeuillez choisir un nombre compris entre 2 et 5 !\n")
        userInput = input("\nCombien de joueurs participent [2/3/4/5] ? ")
        time.sleep(1)

    players_nbr = int(userInput)
    
    # Choice of a nickname for every player
    os.system("cls" if os.name == "nt" else "clear")
    pseudos = []

    for i in range(players_nbr):
        os.system("cls" if os.name == "nt" else "clear")
        print("-"*62,"👾","-"*62)
        print_typing(f"{space('large')}Joueur numéro {i+1}\n") 
        print_typing(f"Choisissez un pseudonyme ? \n")
        choice = input()

        while choice in pseudos:
            print(f"\nErreur, ce pseudonyme a déjà été pris, choisissez-en un autre !")
            choice = input()
        pseudos.append(choice)

    return pseudos

"""
space : returns a string containing a greater or lesser number of spaces
"""
def space(str):
    if str == 'small':
        space_lenght = ' '*45
    elif str == 'medium':
        space_lenght = ' '*50
    elif str == 'large':
        space_lenght = ' '*55
    elif str == 'very_large':
        space_lenght = ' '*58
    return space_lenght

"""
final_result : displays the final scores and compares them to give the final winner
"""
def final_result(pseudos_players, Quiz):
    
    winner=[]
    maximum = 0

    # The scores are displayed and compared to determine the winner
    for j in pseudos_players:
        countries_visited = ", ".join(Quiz[j].validated_countries)

        if len(countries_visited) != 0:
            print_typing("\n".join([f"{j} : {Quiz[j].points}, a parcouru {countries_visited}.\n"]))
        else: 
            print_typing("\n".join([f"{j} : {Quiz[j].points}, n'a rien parcouru.\n"]))

        if Quiz[j].points > maximum and Quiz[j].points != 0:
            winner.append(j)
            maximum = Quiz[j].points

    # The winner is determined by the one with the highest score
    time.sleep(2.5)
    if maximum > 0:
        winner_result = ", ".join(winner)
        print_typing("\n".join([f"{winner_result} gagne(nt) la partie, bravo !\n"]))
    else:
        print_typing("\nDommage, personne n'a gagné !\n")
        