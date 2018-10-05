#!/usr/bin/python
#  -*- coding: utf-8 -*-
import json
from question import Question

class Questionnaire:
    def __init__(self):
        with open('questionnaire/config/questions.json') as question_file:
            json_questionnaire = json.load(question_file)

        self.liste_question={}
        for section in json_questionnaire:
            self.liste_question[section]={}
            for q in json_questionnaire.get(section):
                self.liste_question[section][q]=Question(json_questionnaire.get(section).get(q))

    def __str__(self):
        return str(self.liste_question)

    def get_liste_section(self):
        return self.liste_question.keys()

    ''' RECUPERATION DUNE QUESTION AVEC SON ID '''
    def get_question(self,section_en_cours,question_en_cours):
        return self[section_en_cours][question_en_cours]


