#!/usr/bin/python
#  -*- coding: utf-8 -*-


class Question:
    def __init__(self,data,section_question,q_question):
        self.type=data.get("type")
        self.libelle=data.get("libelle_question")
        self.has_image = data.get("has_image")
        self.image_link = data.get("image_link")
        self.reponse=data.get("reponse")
        self.correct = data.get("correct")
        self.section_question= section_question
        self.q_question = q_question

    def __str__(self):
        return 'Libelle question : {} \n Type question : {} \n has_image : {} \ Reponse : {}  \n Correct : {} '.format(self.libelle,self.type,self.has_image, self.reponse, self.correct)

    ''' 
        Fonction permettant de corriger une question :
            Section :
            Question :
            Réponse du candidat
    '''
    def traitement_une_question(self,reponse_candidat):
        # Si le candidat a répondu à la question
        if self.section_question in reponse_candidat.keys():
            if str(self.q_question) in reponse_candidat[self.section_question] and reponse_candidat[self.section_question][str(self.q_question)]:
                #print '################ REPONSE CANDIDAT ################'
                #print reponse_candidat[section][q]
                #print '################ REPONSE CORRECTE ################'
                #print self.correct

                # Il faut distinguer les différents cas
                if self.type=='button':
                    # Il s'agit d'une comparaison 1 à 1
                    if reponse_candidat[self.section_question][self.q_question]==self.correct:
                        return 'Réponse correcte'
                    else:
                        return 'Réponse incorrecte'

                elif self.type=='checkbox':
                    # Il s'agit d'une comparaison de list
                    if isinstance(reponse_candidat[self.section_question][self.q_question],str):
                        rep_temp=[reponse_candidat[self.section_question][self.q_question]]
                    else:
                        rep_temp=reponse_candidat[self.section_question][self.q_question]
                    if rep_temp==self.correct:
                        return 'Réponse correcte'
                    else:
                        return 'Réponse incorrecte'
                # Si c'est du text on retourne le champs texte
                else:
                    return reponse_candidat[self.section_question][self.q_question]

        return 'Pas de reponse'