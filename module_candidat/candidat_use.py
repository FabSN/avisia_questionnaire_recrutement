#!/usr/bin/python
#  -*- coding: utf-8 -*-
import json

class Candidat:
    def __init__(self,nom_candidat,prenom_candidat='',section_choix=[],id_candidat=None,response={}):
        if isinstance(nom_candidat,dict)==False:
            self.nom_candidat=nom_candidat
            self.prenom_candidat=prenom_candidat
            if isinstance(section_choix,list):
                self.section_choix=section_choix
            else:
                self.section_choix = [section_choix]
            self.id_candidat=id_candidat
            self.response=response

        # Si on charge le fichier de session
        else:
            self.nom_candidat=nom_candidat['nom_candidat']
            self.prenom_candidat=nom_candidat['prenom_candidat']
            self.section_choix=nom_candidat['section_choix']
            self.id_candidat=nom_candidat['id_candidat']
            if "response" in nom_candidat.keys():
                self.response=nom_candidat['response']
            else:
                self.response = response

    def __str__(self):
        return "Nom_candidat : {} \n Prenom candidat : {} \n Section : {} \n id candidat : {}".format(self.nom_candidat,self.prenom_candidat,' '.join(self.section_choix), self.id_candidat)

    '''
        Méthode permettant de transformer un candidat en json
    '''
    def to_json(self):
        sortie_json={}
        sortie_json['nom_candidat']=self.nom_candidat
        sortie_json['prenom_candidat'] = self.prenom_candidat
        sortie_json['section_choix'] = self.section_choix
        sortie_json['id_candidat'] = self.id_candidat
        if self.response:
            sortie_json['response']=self.response
        output=json.dumps(sortie_json)
        return output

    '''
        Méthode  permettant de chercher si le candidat a déjà répondu a une question 
    '''
    def search_response(self,section_en_cours,id_question):
        # Si il a déjà des réponses
        if isinstance(self.response,dict):
            if section_en_cours in self.response.keys():
                if id_question in self.response[section_en_cours].keys():
                    return self.response[section_en_cours][id_question]
        return ''

    ''' 
        Ajout d'une réponse à une question
    '''
    def add_response_question(self,section_en_cours,id_question,reponse):
        if section_en_cours in self.response.keys():
            self.response[section_en_cours][id_question]=reponse
        else:
            self.response[section_en_cours]={}
            self.response[section_en_cours][id_question] = reponse
        return "update OK"

    def nb_rep_par_section(self):
        nb_q_rep_section = {}
        for sec in self.section_choix:
            # Si il a répondu a une question au moins
            if sec in self.response:
                nb_q_rep_section[sec] = len(self.response[sec])
            else:
                nb_q_rep_section[sec]=0
        return nb_q_rep_section
