#!/usr/bin/python
#  -*- coding: utf-8 -*-


class Question:
    def __init__(self,data):
        self.type=data.get("type")
        self.libelle=data.get("libelle_question")
        self.reponse=data.get("reponse")
        self.correct = data.get("correct")

    def __str__(self):
        return 'Libelle question : {} \n Type question : {} \ Reponse : {} \n Correct : {}'.format(self.libelle,self.type, self.reponse, self.correct)
