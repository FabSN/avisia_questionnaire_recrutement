# !/usr/bin/python
# coding: utf8

# Importation des packages
from flask import Flask, render_template, request,redirect,url_for,session
import time
import datetime
import logging as lg
import pandas as pd
import requests

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
    # Home
    return render_template('home.html', section_table=df_sections)

''' Page candidat '''
@app.route('/candidat', methods=['GET', 'POST'])
def candidat():
    # On arrive depuis la page Home
    if request.method == 'POST':
        # Recuperation des variables
        nom_candidat = request.form.get('nom_candidat')
        prenom_candidat = request.form.get('prenom_candidat')
        section_choix = request.form.getlist('section_choix')
        # Recuperation de la liste des sessions dans un dataframe a partir de la variable session
        df_sections_v2=pd.read_json(session['dataframe_section'], orient='records')

        # Stockage du candidat courant dans un dataframe
        session['id_candidat']=interaction_database_app.stockage_candidat(nom_candidat,prenom_candidat,section_choix)
        lg.info('VALEUR ID : {}'.format(session['id_candidat']))
        lg.info('SECTION CHOIX : {}'.format(section_choix))
        return render_template('candidat.html', nom_candidat=nom_candidat,prenom_candidat=prenom_candidat,section_choix=section_choix,df_section=df_sections_v2)
    else:
        return redirect(url_for('index'))

''' Page lancement_questionnaire'''
@app.route('/lancement_questionnaire', methods=['GET', 'POST'])
def lancement_questionnaire():
    # On arrive depuis la page Home
    if request.method == 'POST':
        # Recuperation des variables
        launch_questionnaire = request.form.get('choix_questionnaire')
        print launch_questionnaire
        # Recuperation de la liste des sessions dans un dataframe a partir de la variable session
        df_sections_v2=pd.read_json(session['dataframe_section'], orient='records')

        # Lancement de la bonne page
        for i,liste in df_sections_v2.iterrows():
            print i
            if launch_questionnaire==liste['id_section']:
                if launch_questionnaire=='r001':
                    return redirect('http://google.fr')
                else:
                    return redirect('http://lequipe.fr')
    else:
        return redirect(url_for('index'))


#@app.route('/player/<int:id_player>/')
#def player(id_player):
#    players_table = interaction_database_app.get_players().set_index('id_player')
#    players_stat = interaction_database_app.recup_players_stat()
#    return render_template('player.html', players_table = players_stat, id_player=id_player)


if __name__ == '__main__':
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run(debug=True, host='0.0.0.0', port=1234)
