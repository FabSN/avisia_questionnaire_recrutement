#!/usr/bin/python
#  -*- coding: utf-8 -*-
import json

class Candidat:
    def __init__(self,nom_candidat,prenom_candidat,section_choix):
        self.nom_candidat=nom_candidat
        self.prenom_candidat=prenom_candidat
        self.section_choix=section_choix
        self.id_candidat=1

    def __init__(self,json_info):
        info=json.loads(json_info)
        self.nom_candidat=info['nom_candidat']
        self.prenom_candidat=info['prenom_candidat']
        self.section_choix=info['section_choix']
        self.id_candidat=info['id_candidat']

    def to_json(self):
        sortie_json={}
        sortie_json['nom_candidat']=self.nom_candidat
        sortie_json['prenom_candidat'] = self.prenom_candidat
        sortie_json['section_choix'] = self.section_choix
        sortie_json['id_candidat'] = self.id_candidat
        output=json.dumps(sortie_json)
        return output