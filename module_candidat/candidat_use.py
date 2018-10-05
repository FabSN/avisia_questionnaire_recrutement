#!/usr/bin/python
#  -*- coding: utf-8 -*-
import json

class Candidat:
    def __init__(self,nom_candidat,prenom_candidat,section_choix,id_candidat=None,response=None):
        self.nom_candidat=nom_candidat
        self.prenom_candidat=prenom_candidat
        if isinstance(section_choix,list):
            self.section_choix=section_choix
        else:
            self.section_choix = [section_choix]
        self.id_candidat=id_candidat
        self.response=response

    def __str__(self):
        return "Nom_candidat : {} \n Prenom candidat : {} \n Section : {} \n id candidat : {}".format(self.nom_candidat,self.prenom_candidat,' '.join(self.section_choix), self.id_candidat)

    def to_json(self):
        sortie_json={}
        sortie_json['nom_candidat']=self.nom_candidat
        sortie_json['prenom_candidat'] = self.prenom_candidat
        sortie_json['section_choix'] = self.section_choix
        sortie_json['id_candidat'] = self.id_candidat
        output=json.dumps(sortie_json)
        return output


    def search_response(self,section_en_cours,id_question):
        # Si il a déjà des réponses
        if isinstance(self.response,dict):
            if section_en_cours in self.response.keys():
                if id_question in self.response[section_en_cours].keys():
                    return self.response[section_en_cours][id_question]
        return None
