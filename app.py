# !/usr/bin/python
# coding: utf8

# Importation des packages
from flask import Flask, render_template, request,redirect,url_for,session
import logging as lg
import json

# Custom module
from module_questionnaire import questionnaire
from module_candidat import candidat_use

# Initialisation du questionnaire
global dict_question
dict_question = questionnaire.Questionnaire()

# Lancement app
app = Flask(__name__)

''' @index
        Page d'accueil du questionnaire
        Il faut compléter nom + prénom + choisir au moins un des champs        
'''
@app.route('/')
def index():
    session['candidat']=''
    return render_template('home.html', section_table=dict_question.get_liste_section())

''' Page candidat '''
@app.route('/candidat', methods=['GET', 'POST'])
def candidat():
    # On arrive depuis la page Home
    if request.method == 'POST':
        if request.form.get('section_choix')==None:
            return redirect(url_for('index'))
        else:
            # Création d'un user
            candidat_en_cours=candidat_use.Candidat(request.form.get('nom_candidat'), request.form.get('prenom_candidat'), request.form.getlist('section_choix'))
            # Sauvegarde dans la session
            session['candidat']=candidat_en_cours.to_json()
            return render_template('candidat.html',candidat=candidat_en_cours)

    # Si on arrive avec un get et qu'il y a un id_candidat dans la session alors on affiche la liste des sections
    elif request.method == 'GET' and session['candidat']<>'':
        json_candidat = json.loads(session['candidat'])
        candidat_en_cours=candidat_use.Candidat(json_candidat)
        return render_template('candidat.html',candidat=candidat_en_cours)
    # Sinon on renvoit l'accueil car on a rien à faire là
    else:
        return redirect(url_for('index'))


''' Page de lancement_questionnaire '''
''' Page de transition que l'on appelle depuis la page candidat avec une valeur du choix de la section'''
''' Cette page fait juste une redirection vers la première question de la section sélectionnée '''
@app.route('/lancement_questionnaire', methods=['GET', 'POST'])
def lancement_questionnaire():
    # On arrive depuis la page Candidat
    if request.method == 'POST':
        launch_questionnaire = request.form.get('choix_questionnaire')
        return redirect(url_for('question'
                                ,section_en_cours=launch_questionnaire
                                ,id_question='1'))
    else:
        return redirect(url_for('index'))


''' Affichage de la question i de la section choisit '''
@app.route('/question/<string:section_en_cours>/<string:id_question>/vars', methods=['GET', 'POST'])
def question(section_en_cours,id_question):
    if request.method == 'GET' and session['candidat']<>'':
        # search response
        json_candidat = json.loads(session['candidat'])
        candidat_en_cours=candidat_use.Candidat(json_candidat)
        return render_template('question.html'
                    , json_question= dict_question.get_question(section_en_cours,id_question)
                    , reponse_candidat_html=candidat_en_cours.search_response(section_en_cours,id_question)
                    , id_question=id_question
                    , section_en_cours=section_en_cours
                    )

    # pas un vrai candidat actif donc retour accueil
    elif request.method == 'GET' and session['id_candidat'] == '':
        return redirect(url_for('index'))

    # On arrive avec un POST quand il y a validation de la question précédente
    elif request.method == 'POST':
        # Si plus de 1 réponse alors checkbox donc on récupère dans getlist sinon avec get
        if len(request.form.getlist('choix_reponse'))>1:
            reponse=request.form.getlist('choix_reponse')
        else:
            reponse=request.form.get('choix_reponse')

        # Ajout de la réponse sur le candidat
        json_candidat = json.loads(session['candidat'])
        candidat_en_cours=candidat_use.Candidat(json_candidat)
        candidat_en_cours.add_response_question(section_en_cours, id_question, reponse)
        session['candidat'] = candidat_en_cours.to_json()

        # Recherche si il y a une question suivante dans la partie
        question_suivante = dict_question.get_question(request.form.get('section_en_cours')
                                                       , int(request.form.get('id_question'))+1)

        # On vérifie si il y a une question suivante pour faire la redirection qui va bien.
        if isinstance(question_suivante,str)==False:
            id_question_suivante=int(request.form.get('id_question'))+1
            return redirect(url_for('question'
                                    , json_question=dict_question.get_question(section_en_cours, id_question_suivante)
                                    , reponse_candidat_html=candidat_en_cours.search_response(section_en_cours,id_question_suivante)
                                    ,id_question=id_question_suivante
                                    ,section_en_cours=request.form.get('section_en_cours')))
        else:
            return redirect(url_for('candidat'))


''' Validation questionnaire'''
@app.route('/validation_questionnaire', methods=['GET'])
def validation_questionnaire():
    # On arrive depuis la page Candidat
    if session['candidat']<>'':
        dict_question.validation_questionnaire(session['candidat'])
        return redirect(url_for('candidat'))
    else:
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run(debug=True, host='0.0.0.0', port=1234)
