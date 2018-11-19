#!/usr/bin/python
#  -*- coding: utf-8 -*-
import json
from question import Question
from flask_mail import Mail,Message
import os
from fpdf import FPDF
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4


class Questionnaire:
    def __init__(self):
        with open('module_questionnaire/config/questions.json') as question_file:
            json_questionnaire = json.load(question_file)
        self.liste_question={}
        self.nb_question_par_section={}
        for section in json_questionnaire:
            self.liste_question[section]={}
            for q in json_questionnaire.get(section):
                self.liste_question[section][q]=Question(json_questionnaire.get(section).get(q),section,q)

                # Pour detreminer le nombre de  question par section
                if section in self.nb_question_par_section:
                    self.nb_question_par_section[section]=self.nb_question_par_section[section]+1
                else:
                    self.nb_question_par_section[section] = 1

    def __str__(self):
        output=''
        for sec in self.liste_question:
            output=output+ '#######################' + '\n'
            output=output+ ' ' + sec + ' nb questions : '+ str(self.nb_question_par_section[sec]) + '\n'

            liste_num_question=[]
            for i in self.liste_question[sec]:
                liste_num_question=liste_num_question+[int(i)]
            for ques in range(1,int(max(liste_num_question))+1):
                output=output + '        q : ' + str(ques) + '\n'
                output = output + '                Libelle : ' + str(self.liste_question[sec][str(ques)].libelle) + '\n'
        return output

    ''' 
        Recuperation de la liste des sections
    '''
    def get_liste_section(self):
        return self.liste_question.keys()

    '''
        Récupération d'une question par rapport à la section et la question
    '''
    def get_question(self,section_en_cours,question_en_cours):
        print section_en_cours, question_en_cours
        if section_en_cours in self.liste_question.keys():
            if str(question_en_cours) in self.liste_question[section_en_cours].keys():
                return self.liste_question[section_en_cours][str(question_en_cours)]
            else:
                return 'NO'

    '''
        Validation questionnaire :
            Fonction de correction du questionnaire
            @resultat : dictionnaire d'un candidat à corriger
    '''
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


        # Creqtion du fichier pdf
        pdf_name = "CORRECTION_TEST"
        c = canvas.Canvas(pdf_name+'.pdf')

        # Variable declarée pour verifiier si les réponses python ont été afficher
        # Les réponses sont affichés sur une seule page au vu de la taille
        # Les autres reponses sont affichés ( 2 sections par page)

        global is_python_page_displayed
        is_python_page_displayed=False

        # Section affichée precedemment
        previous_section = ''
        # Section affichée precedemment
        section_rank=1
        # Nombre de sections sur une page
        global number_of_section_on_page
        number_of_section_on_page= 0
        # Dimensions des pages
        heigth = 750
        width = 15


        for section in json_resultat['section_choix']:
            current_section = section

            # Verification afficahe de la section python premiere page
            if section == "Python" and section_rank == 1:
                heigth = 750
                width = 15
                is_python_page_displayed = True

            # Verification afficahe de la section python après premiere page
            if section == "Python" and section_rank > 1:
                c.showPage()
                heigth = 750
                width = 15
                is_python_page_displayed = True

            # Reduire la hauteur de lignes et affichage
            heigth = heigth - 30
            c.setFont('Helvetica', 15)
            c.drawString(width+215, heigth, section.upper())
            heigth = heigth - 40


            print "################################"
            print "SECTION : {}".format(section)
            print "################################"
            liste=[int(i) for i in self.liste_question[section]]
            for q in sorted(liste):
                #print "Question : {} \n Correction : {} \n".format(compilation_reponse[section][str(q)]['question'],compilation_reponse[section][str(q)]['correction'])
                # v = "Question : {} \n Correction : {} \n".format(compilation_reponse[section][str(q)]['question'],compilation_reponse[section][str(q)]['correction'])
                print compilation_reponse[section][str(q)]['question']
                print compilation_reponse[section][str(q)]['correction']

                # Reduire la hauteur de lignes et affichage
                c.setFont('Helvetica-Bold', 10)
                c.drawString(width, heigth, "Question :"+compilation_reponse[section][str(q)]['question'])
                heigth = heigth - 20
                c.setFont('Helvetica', 10)
                c.drawString(width, heigth, "Reponse :"+compilation_reponse[section][str(q)]['correction'])
                heigth = heigth - 20

            # Afficher 2 section par page
            print "section_rank=", section_rank,
            if section != "Python":
                if previous_section == "Python":
                    number_of_section_on_page=0
                number_of_section_on_page+= 1
                if number_of_section_on_page == 2:
                    c.showPage()
                    heigth = 750
                    width = 15
                    number_of_section_on_page=0

            #Si la section est python afficher sur une nouvelle page pdf directement à cause de la taille
            if section == "Python":
                c.showPage()
                heigth = 750
                width = 15
                is_python_page_displayed = True

            previous_section = current_section
            section_rank = section_rank + 1

        c.save()





