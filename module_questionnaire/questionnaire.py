#!/usr/bin/python
#  -*- coding: utf-8 -*-
import json
from question import Question

class Questionnaire:
    def __init__(self):
        with open('module_questionnaire/config/questions.json') as question_file:
            json_questionnaire = json.load(question_file)

        self.liste_question={}
        for section in json_questionnaire:
            self.liste_question[section]={}
            for q in json_questionnaire.get(section):
                self.liste_question[section][q]=Question(json_questionnaire.get(section).get(q))

    def __str__(self):
        return str(self.liste_question)

    ''' 
        Recuperation de la liste des sections
    '''
    def get_liste_section(self):
        return self.liste_question.keys()

    '''
        Récupération d'une question par rapport à la section et la question
    '''
    def get_question(self,section_en_cours,question_en_cours):
        if section_en_cours in self.liste_question.keys():
            if str(question_en_cours) in self.liste_question[section_en_cours].keys():
                return self.liste_question[section_en_cours][str(question_en_cours)]
            else:
                return 'NO'

    def validation_questionnaire(self,resultat):
        json_resultat=json.loads(resultat)
        reponse=json_resultat['response']
        for section in json_resultat['section_choix']:
            print section
            for q in self.liste_question[section]:
                print '################ REPONSE CORRECTE ################'
                print self.liste_question[section][q].correct
                if section in reponse.keys():
                    if reponse[section][q]:
                        print '################ REPONSE CANDIDAT ################'
                        print reponse[section][q]
                        if self.liste_question[section][q].correct==reponse[section][q]:
                            print 'CORRECT'
                        else:
                            print 'FAUX'
                else:
                    print 'FAUX'




