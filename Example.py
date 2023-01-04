# -*- coding: utf-8 -*-
"""
Created on Thu Dec 22 21:55:11 2022

@author: Admin
"""

from Quiz import Quiz
from sparQL_query import Question_corpus

Q = Quiz(None,Question_corpus)
Q.next_question()
Q.next_question()
Q.next_country()
Q.next_question()
Q.next_country()