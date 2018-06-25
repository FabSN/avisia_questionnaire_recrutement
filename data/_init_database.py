#!/usr/bin/python
# coding: utf8

# Chargement des packages
import sys
import logging as lg
import sqlite3 as sql
import time
import datetime
import pandas as pd
import json

sys.path.append("data")
import fonction_database

# Initialisation de la log
t = datetime.datetime.now()
fn = 'logs/init_db.{}.log'.format(t.strftime("%Y-%m-%d"))
lg.basicConfig(filename=fn,
               level=lg.DEBUG,
               filemode='a',
               format='%(asctime)s\t%(levelname)s\t%(message)s',
               datefmt='%Y-%m-%d %H:%M:%S'
               )

# Chargement du fichier de config
try:
    lg.info("Chargement de la base à partir du fichier de configuration")
    with open('config.json') as conf_file:
        global DB
        DB = json.load(conf_file)
except:
    lg.info("Erreur lors du chargement de la base à partir du fichier de configuration")


lg.info("Ouverture de la base")
connexion, requete = fonction_database.fonction_connexion_sqllite()

# Initialisation de la fonction de création des tables
def CreateTable():
    # Création de la candidats_en_cours
    requete.execute('''DROP TABLE IF EXISTS candidats_en_cours;''')
    requete.execute('''CREATE TABLE IF NOT EXISTS `candidats_en_cours` ( `id_candidat` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, `prenom_candidat` TEXT NOT NULL, `nom_candidat` TEXT NOT NULL, `section_candidat` TEXT NOT NULL )''')
    # Table des réponses à chaque question du candidat en cours
    requete.execute('''DROP TABLE IF EXISTS candidats_reponses_questions;''')
    requete.execute('''CREATE TABLE IF NOT EXISTS `candidats_reponses_questions` ( `id_reponse` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, `foreign_id_candidat` INTEGER NOT NULL, `foreign_id_question` INTEGER NOT NULL, `reponse_question_candidat` INTEGER, FOREIGN KEY(`foreign_id_question`) REFERENCES `ref_questions`(`id_question`), FOREIGN KEY(`foreign_id_candidat`) REFERENCES `candidats_en_cours`(`id_candidat`))''')


    # Referentiel des questions
    requete.execute('''DROP TABLE IF EXISTS ref_questions;''')
    requete.execute('''CREATE TABLE IF NOT EXISTS `ref_questions` ( `id_question` TEXT NOT NULL, `ref_id_section` TEXT, `libelle_question` TEXT, `type_formulaire_question` TEXT, `liste_reponses_questions` TEXT, `bonne_reponse_question` TEXT, FOREIGN KEY(`ref_id_section`) REFERENCES `ref_sections`(`id_section`), PRIMARY KEY(`id_question`))''')

    # Referentiel des sections du QCM
    requete.execute('''DROP TABLE IF EXISTS ref_sections;''')
    requete.execute('''CREATE TABLE IF NOT EXISTS "ref_sections" ( `id_section` TEXT NOT NULL, `libelle_section` TEXT NOT NULL, `image_section` TEXT, PRIMARY KEY(`id_section`))''')
    requete.execute('''INSERT INTO ref_sections (id_section,libelle_section,image_section) VALUES ('py001','Python','python.jpg');''')
    requete.execute('''INSERT INTO ref_sections (id_section,libelle_section,image_section) VALUES ('r001','R','r.jpg');''')
    requete.execute('''INSERT INTO ref_sections (id_section,libelle_section,image_section) VALUES ('sas001','SAS','sas.jpg');''')
    requete.execute('''INSERT INTO ref_sections (id_section,libelle_section,image_section) VALUES ('metier001','MARKETING','marketing.jpg');''')

# Appel de la fonction de création des tables
lg.info("Création des tables")
CreateTable()

lg.info("Fermeture de la base")
fonction_database.fonction_connexion_sqllite_fermeture(connexion, requete)
lg.info("Fin d'initialisation des tables dans la base")
