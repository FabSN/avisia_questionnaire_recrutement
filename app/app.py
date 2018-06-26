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
    # Recup des sessions disponibles
    df_sections = interaction_database_app.get_section()
    # Stockage dans une variable de session
    session['dataframe_section']=df_sections.to_json(orient='records')
    session['id_candidat']=''
    session['nom_candidat'] = ''
    session['prenom_candidat'] = ''
    session['section_choix'] = ''
    # Home
    return render_template('home.html', section_table=df_sections)

''' Page candidat '''
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

    elif request.method == 'GET' and session['id_candidat']<>'':
        df_sections_v2 = pd.read_json(session['dataframe_section'], orient='records')
        return render_template('candidat.html', nom_candidat=session['nom_candidat']
                                              , prenom_candidat=session['prenom_candidat']
                                              ,section_choix=session['section_choix']
                                              , df_section=df_sections_v2)
    else:
        return redirect(url_for('index'))


''' Page lancement_questionnaire'''
@app.route('/lancement_questionnaire', methods=['GET', 'POST'])
def lancement_questionnaire():
    # On arrive depuis la page Home
    if request.method == 'POST':
        # Recuperation des variables
        launch_questionnaire = request.form.get('choix_questionnaire')
        return redirect(url_for('question',id_question=launch_questionnaire+'_001'))
    else:
        return redirect(url_for('index'))


@app.route('/question/<string:id_question>/', methods=['GET', 'POST'])
def question(id_question):
    # On arrive avec un GET depuis la page candidat
    if request.method == 'GET' and session['id_candidat']<>'':
        lg.info("lancement de la question "+id_question)
        # Recupération de la question
        json_question_app = interaction_database_app.get_question(id_question)

        # Recuperation de la reponse du candidat si il y en a une
        reponse_candidat_app=interaction_database_app.get_reponse_question(id_question=id_question,id_candidat=session['id_candidat'])
        print "reponse "+str(reponse_candidat_app)
        return render_template('question.html', json_question= json_question_app,reponse_candidat_html=str(reponse_candidat_app))

    elif request.method == 'GET' and session['id_candidat'] == '':
        return redirect(url_for('index'))
    # On arrive avec un POST quand il y a validation de la question
    elif request.method == 'POST':
        # Insertion de la réponse
        interaction_database_app.insert_or_update_reponse_question(id_question=request.form.get('id_question')
                                                       , reponse_question_candidat=request.form.get('choix_reponse')
                                                       , id_candidat=session['id_candidat'][0])

        # Recherche si il y a une question suivante dans la partie
        flag_question_suivante=interaction_database_app.check_question_suivante(section_recherche=request.form.get('id_section')
                                                        ,question_en_cours=request.form.get('id_question'))

        if flag_question_suivante==1:
            # Calcul de l'id de la question suivante
            question_en_cours=request.form.get('id_question')
            question_suivante = question_en_cours.split('_')[0] + '_' + '{0:03}'.format(int(question_en_cours.split('_')[1]) + 1)
            return redirect(url_for('question',id_question=question_suivante))
        else:
            return redirect(url_for('candidat'))

if __name__ == '__main__':
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run(debug=True, host='0.0.0.0', port=1234)
