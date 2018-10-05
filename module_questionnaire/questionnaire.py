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

        compilation_reponse={}
        for section in json_resultat['section_choix']:
            compilation_reponse[section]={}
            for q in self.liste_question[section]:
                question_courante=self.liste_question[section][q]
                sortie={}
                sortie['correction']=question_courante.traitement_une_question(section,q,reponse)
                sortie['question']=question_courante.libelle
                compilation_reponse[section][q]=sortie

        ###########################
        # Affichage des résultats
        ###########################
        for section in json_resultat['section_choix']:
            print "################################"
            print "SECTION : {}".format(section)
            print "################################"
            liste=[int(i) for i in self.liste_question[section]]
            for q in sorted(liste):
                print "Question : {} \n Correction : {} \n".format(compilation_reponse[section][str(q)]['question'],compilation_reponse[section][str(q)]['correction'])




