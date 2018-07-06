# !/usr/bin/python
# coding: utf8

# Importation des packages
from flask import Flask, render_template, request,redirect,url_for,session
import time
import datetime
import logging as lg
import pandas as pd
import requests
import json

# Custom package
import sys
sys.path.append('app/lib')
import interaction_database_app

# Initialisation de la log
t = datetime.datetime.now()
fn = 'logs/run_flask.{}.log'.format(t.strftime("%Y-%m-%d"))
lg.basicConfig(filename = fn,
               level = lg.INFO,
               filemode = 'a',
               format = '%(asctime)s\t%(levelname)s\t%(message)s',
               datefmt = '%Y-%m-%d %H:%M:%S'
               )


###############################
# Lancement app
###############################
app = Flask(__name__)


''' Page d'accueil '''
@app.route('/')
def index():
    # Recup des sections disponibles : R PYTHON ...
    df_sections = interaction_database_app.get_section()
    # Stockage dans une variable de session
    # Variable disponible toute la session du user dont on initialise sur la page d'accueil car on stockera ensuite l'id candidat...
    session['dataframe_section']=df_sections.to_json(orient='records')
    session['id_candidat']=''
    session['nom_candidat'] = ''
    session['prenom_candidat'] = ''
    session['section_choix'] = ''
    # Home
    return render_template('home.html', section_table=df_sections)

''' Page candidat '''
''' Page contenant les sections sélectionnées pour le candidat'''
@app.route('/candidat', methods=['GET', 'POST'])
def candidat():
    # On arrive depuis la page Home
    if request.method == 'POST':
        # Recuperation des variables
        nom_candidat = request.form.get('nom_candidat')
        session['nom_candidat']=nom_candidat
        prenom_candidat = request.form.get('prenom_candidat')
        session['prenom_candidat'] = prenom_candidat
        section_choix = request.form.getlist('section_choix')
        session['section_choix'] = section_choix
        # Recuperation de la liste des sessions dans un dataframe a partir de la variable session
        df_sections_v2=pd.read_json(session['dataframe_section'], orient='records')

        # Stockage du candidat courant dans un dataframe
        session['id_candidat']=interaction_database_app.stockage_candidat(nom_candidat,prenom_candidat,section_choix)
        lg.info('VALEUR ID : {}'.format(session['id_candidat']))
        lg.info('SECTION CHOIX : {}'.format(section_choix))
        return render_template('candidat.html', nom_candidat=nom_candidat,prenom_candidat=prenom_candidat,section_choix=section_choix,df_section=df_sections_v2)

    # Si on arrive avec un get et qu'il y a un id_candidat dans la session alors on affiche la liste des sections
    elif request.method == 'GET' and session['id_candidat']<>'':
        df_sections_v2 = pd.read_json(session['dataframe_section'], orient='records')
        return render_template('candidat.html', nom_candidat=session['nom_candidat']
                                              , prenom_candidat=session['prenom_candidat']
                                              ,section_choix=session['section_choix']
                                              , df_section=df_sections_v2)
    # Sinon on renvoit l'accueil car on a rien à faire là
    else:
        return redirect(url_for('index'))


''' Page lancement_questionnaire'''
''' Page de transition que l'on appelle depuis la page candidat avec une valeur du choix de la section'''
''' Cette page fait juste une redirection vers la première question de la section sélectionnée '''
@app.route('/lancement_questionnaire', methods=['GET', 'POST'])
def lancement_questionnaire():
    # On arrive depuis la page Home
    if request.method == 'POST':
        # Recuperation des variables
        launch_questionnaire = request.form.get('choix_questionnaire')
        return redirect(url_for('question',id_question=launch_questionnaire+'_001'))
    else:
        return redirect(url_for('index'))


''' Affichage de la question i de la section choisit '''
@app.route('/question/<string:id_question>/', methods=['GET', 'POST'])
def question(id_question):
    # On arrive avec un GET depuis la page candidat
    if request.method == 'GET' and session['id_candidat']<>'':
        lg.info("lancement de la question "+id_question)
        # Recupération de la question
        json_question_app = interaction_database_app.get_question(id_question)
        # Recuperation de la reponse du candidat si il y en a une
        reponse_candidat_app=interaction_database_app.get_reponse_question(id_question=id_question,id_candidat=session['id_candidat'])
        return render_template('question.html', json_question= json_question_app,reponse_candidat_html=str(reponse_candidat_app))

    # pas un vrai candidat actif donc retour accueil
    elif request.method == 'GET' and session['id_candidat'] == '':
        return redirect(url_for('index'))
    # On arrive avec un POST quand il y a validation de la question précédente
    elif request.method == 'POST':
        ##  Insertion de la réponse
        # différent si il s'agit d'uncheckbox ou d'un button
        # Si plus de 1 réponse alors checkbox donc on récupère dans getlist sinon avec get
        if len(request.form.getlist('choix_reponse'))>1:
            reponse=request.form.getlist('choix_reponse')
            reponse="&".join(reponse)
        else:
            reponse=request.form.get('choix_reponse')

        interaction_database_app.insert_or_update_reponse_question(id_question=request.form.get('id_question')
                                                       , reponse_question_candidat=reponse
                                                       , id_candidat=session['id_candidat'][0])

        # Recherche si il y a une question suivante dans la partie
        flag_question_suivante=interaction_database_app.check_question_suivante(section_recherche=request.form.get('id_section')
                                                        ,question_en_cours=request.form.get('id_question'))

        # On vérifie si il y a une question suivante pour faire la redirection qui va bien.
        #   Question suivante
        #   Page candidat sinon
        if flag_question_suivante==1:
            # Calcul de l'id de la question suivante
            question_en_cours=request.form.get('id_question')
            question_suivante = question_en_cours.split('_')[0] + '_' + '{0:03}'.format(int(question_en_cours.split('_')[1]) + 1)
            return redirect(url_for('question',id_question=question_suivante))
        else:
            return redirect(url_for('candidat'))


''' Page ajout_question'''
@app.route('/ajout_question', methods=['GET', 'POST'])
def ajout_question():
    # On arrive depuis la page Home
    if request.method == 'POST':
        # Recuperation des variables
        section_choix = request.form.get('section_choix')
        libelle_question = request.form.get('libelle_question')
        type_question=request.form.get('type_question')
        reponse1=request.form.get('reponse1')
        reponse2=request.form.get('reponse2')
        reponse3=request.form.get('reponse3')
        reponse4=request.form.get('reponse4')

        statut=interaction_database_app.insert_question(section_choix,libelle_question,type_question,reponse1,reponse2,reponse3,reponse4)

        df_sections = interaction_database_app.get_section()
        return render_template('ajout_question.html', section_table=df_sections)
    else:
        df_sections = interaction_database_app.get_section()
        return render_template('ajout_question.html',section_table=df_sections)

if __name__ == '__main__':
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run(debug=True, host='0.0.0.0', port=1234)
