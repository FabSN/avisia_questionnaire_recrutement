# !/usr/bin/python
# coding: utf8

import sys
sys.path.append("data")
import fonction_database
import pandas as pd
import datetime
import time
import logging as lg
import ast
import json


# Retrieve data from database
''' FONCTION PERMETTANT DE RECUPERER LA LISTE DES SECTIONS DE LA TABLE DE REF'''
def get_section():
    #Load Section Table
    cur,conn= fonction_database.fonction_connexion_sqllite()
    query = "SELECT * FROM REF_SECTIONS"
    df_sections = pd.read_sql(query, conn)
    fonction_database.fonction_connexion_sqllite_fermeture(cur,conn)
    lg.info('RECUPERATION DE LA LISTE DES SECTIONS OK')
    return df_sections

''' FONCTION DE STOCKAGE D'UN CANDIDAT '''
def stockage_candidat(nom,prenom,section):
    cur, conn = fonction_database.fonction_connexion_sqllite()
    cur.execute("INSERT INTO candidats_en_cours(prenom_candidat,nom_candidat,section_candidat) VALUES((?), (?),(?));", (str(nom), str(prenom),str(section)))
    cur.execute("SELECT max(id_candidat) FROM candidats_en_cours;")
    id_candidat = cur.fetchone()
    fonction_database.fonction_connexion_sqllite_fermeture(cur,conn)
    lg.info('AJOUT DU CANDIDAT')
    return id_candidat

''' ENCODING POUR LES ACCENTS A ETOFFER '''
def encoding_modif_html(var):
    return var.replace('\\u00e9','&eacute;')

''' RECUPERATION DUNE QUESTION AVEC SON ID '''
def get_question(id):
    cur, conn = fonction_database.fonction_connexion_sqllite()
    df_question=pd.read_sql("SELECT * FROM ref_questions WHERE id_question = '{}';".format(id),conn)
    fonction_database.fonction_connexion_sqllite_fermeture(cur,conn)
    # Si pas de réponse bonne alors null
    df_question['bonne_reponse_question']=df_question['bonne_reponse_question'].apply(lambda x : 99 if x is None else x)
    json_question=df_question.loc[0].to_json()
    json_question=ast.literal_eval(json_question)
    json_question['liste_reponses_questions']=ast.literal_eval(json_question['liste_reponses_questions'])
    json_question['libelle_question']=encoding_modif_html(json_question['libelle_question'])

    for i in json_question['liste_reponses_questions'].keys():
        json_question['liste_reponses_questions'][i]=json_question['liste_reponses_questions'][i].replace('\n','<br>')
        json_question['liste_reponses_questions'][i]=encoding_modif_html(json_question['liste_reponses_questions'][i])

    return json_question

''' AJOUT DE LA REPONSE A LA QUESTION DUN CANDIDAT'''
def insert_or_update_reponse_question(id_question, reponse_question_candidat, id_candidat):
    # On regarde si il faut faire un insert ou un update
    cur, conn = fonction_database.fonction_connexion_sqllite()
    query = "SELECT count(*) as nb FROM candidats_reponses_questions WHERE foreign_id_candidat = '{}' AND foreign_id_question='{}'".format(id_candidat, id_question)
    # print query
    cur.execute(query)
    result = cur.fetchone()
    number_of_rows = result[0]
    fonction_database.fonction_connexion_sqllite_fermeture(cur, conn)

    # Alors il faut faire un update de la réponse
    if number_of_rows==1:
        cur, conn = fonction_database.fonction_connexion_sqllite()
        cur.execute("UPDATE candidats_reponses_questions SET reponse_question_candidat='{}' WHERE foreign_id_candidat={} AND foreign_id_question='{}';".format(str(reponse_question_candidat),int(id_candidat), str(id_question)))
        fonction_database.fonction_connexion_sqllite_fermeture(cur,conn)
    else:
        cur, conn = fonction_database.fonction_connexion_sqllite()
        cur.execute("INSERT INTO candidats_reponses_questions(foreign_id_candidat,foreign_id_question,reponse_question_candidat) VALUES((?), (?),(?));", (int(id_candidat), str(id_question),str(reponse_question_candidat)))
        fonction_database.fonction_connexion_sqllite_fermeture(cur,conn)
    return 'ok'

''' VALIDATION SI IL Y A UNE QUESTION SUIVANTE OU NON '''
def check_question_suivante(section_recherche,question_en_cours):
    # Calcul de l'id de la question suivante
    question_suivante=question_en_cours.split('_')[0]+'_'+'{0:03}'.format(int(question_en_cours.split('_')[1])+1)

    # On regarde si il y au ne question suivante ou pas
    cur, conn = fonction_database.fonction_connexion_sqllite()
    query="SELECT count(*) as nb FROM ref_questions WHERE ref_id_section = '{}' AND id_question='{}'".format(section_recherche,question_suivante)
    #print query
    cur.execute(query)
    result=cur.fetchone()
    number_of_rows = result[0]
    fonction_database.fonction_connexion_sqllite_fermeture(cur,conn)

    # Retourne 1 si une question 0 sinon
    return number_of_rows


''' OBTENIR LA REPONSE DUNE QUESTION DU CANDIDAT'''
def get_reponse_question(id_question,id_candidat):
    # On regarde si il faut faire un insert ou un update
    cur, conn = fonction_database.fonction_connexion_sqllite()
    query = "SELECT count(*) as nb FROM candidats_reponses_questions WHERE foreign_id_candidat = '{}' AND foreign_id_question='{}'".format(id_candidat[0], id_question)
    print query
    cur.execute(query)
    result = cur.fetchone()
    number_of_rows = result[0]
    fonction_database.fonction_connexion_sqllite_fermeture(cur, conn)

    # Le candidat a repondu
    if number_of_rows==1:
        cur, conn = fonction_database.fonction_connexion_sqllite()
        query = "SELECT reponse_question_candidat as nb FROM candidats_reponses_questions WHERE foreign_id_candidat = '{}' AND foreign_id_question='{}'".format(id_candidat[0], id_question)
        cur.execute(query)
        result = cur.fetchone()
        reponse_candidat = result[0]
        reponse_candidat=str(reponse_candidat).split('&')
        fonction_database.fonction_connexion_sqllite_fermeture(cur, conn)
    else:
        reponse_candidat=['9999']
    return reponse_candidat



''' Ajouter une question'''
def insert_question(section_choix, libelle_question, type_question,reponse1,reponse2,reponse3,reponse4):
    # On récupère les id des questions de la section
    cur, conn = fonction_database.fonction_connexion_sqllite()
    query = "SELECT * FROM ref_questions WHERE ref_id_section = '{}';".format(section_choix)
    liste_questions=pd.read_sql(query, conn)
    fonction_database.fonction_connexion_sqllite_fermeture(cur, conn)

    # Si il y a deja des questions
    if liste_questions.shape[0]>0:
        liste_questions['id_question_next']=liste_questions['id_question'].apply(lambda x : int(x.split('_')[-1]))
        question_suivante=section_choix+'_'+'{0:03}'.format(liste_questions['id_question_next'].max()+1)
    else:
        question_suivante = section_choix + '_' + '{0:03}'.format(1)

    dict_reponses={}
    dict_reponses["1"] = reponse1
    dict_reponses["2"] = reponse2
    dict_reponses["3"] = reponse3
    dict_reponses["4"] = reponse4

    json_reponses=json.dumps(dict_reponses)
    cur, conn = fonction_database.fonction_connexion_sqllite()
    cur.execute("INSERT INTO ref_questions(id_question,ref_id_section,libelle_question,type_formulaire_question,liste_reponses_questions) VALUES((?), (?),(?), (?),(?));", (question_suivante, section_choix,libelle_question,type_question,json_reponses))
    fonction_database.fonction_connexion_sqllite_fermeture(cur,conn)

    return 'ok'
