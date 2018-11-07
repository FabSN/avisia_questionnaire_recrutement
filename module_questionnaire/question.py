#!/usr/bin/python
#  -*- coding: utf-8 -*-


class Question:
    def __init__(self,data):
        self.type=data.get("type")
        self.libelle=data.get("libelle_question")
        self.has_image = data.get("has_image")
        self.image_link = data.get("image_link")
        self.reponse=data.get("reponse")
        self.correct = data.get("correct")

    def __str__(self):
        return 'Libelle question : {} \n Type question : {} \n has_image : {} \ Reponse : {}  \n Correct : {} '.format(self.libelle,self.type,self.has_image, self.reponse, self.correct)


    def traitement_une_question(self,section,q,reponse_candidat):
        print  reponse_candidat.keys()

        # Si le candidat a répondu à la question
        if section in reponse_candidat.keys():
            if reponse_candidat[section][q]:
                #print '################ REPONSE CANDIDAT ################'
                #print reponse_candidat[section][q]
                #print '################ REPONSE CORRECTE ################'
                #print self.correct

                # Il faut distinguer les différents cas
                if self.type=='button':
                    # Il s'agit d'une comparaison 1 à 1
                    if reponse_candidat[section][q]==self.correct:
                        #print 'OK : REPONSE CORRECTE ################'
                        return 'Réponse correcte'
                    else:
                        return 'Réponse incorrecte'

                elif self.type=='checkbox':
                    # Il s'agit d'une comparaison de list
                    if isinstance(reponse_candidat[section][q],str):
                        rep_temp=[reponse_candidat[section][q]]
                    else:
                        rep_temp=reponse_candidat[section][q]
                    if rep_temp==self.correct:
                        #print 'OK : REPONSE CORRECTE ################'
                        return 'Réponse correcte'
                    else:
                        return 'Réponse incorrecte'
                # Si c'est du text on retourne le champs texte
                else:
                    return reponse_candidat[section][q]

        return 'Pas de reponse'