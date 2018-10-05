# !/usr/bin/python
# coding: utf8

# Importation des packages
from flask import Flask, render_template, request,redirect,url_for,session
import logging as lg
from module_questionnaire import questionnaire
from module_candidat import candidat_use

###############################
# Lancement app
app = Flask(__name__)

# Initialisation du questionnaire
global dict_question
dict_question=questionnaire.Questionnaire()


''' Page d'accueil '''
@app.route('/')
def index():
    return render_template('home.html'
                          , section_table=dict_question.get_liste_section())

''' Page candidat '''
@app.route('/candidat', methods=['GET', 'POST'])
def candidat():
    # On arrive depuis la page Home
    if request.method == 'POST':
        # Recuperation des variables
        candidat_en_cours=candidat_use.Candidat(request.form.get('nom_candidat'), request.form.get('prenom_candidat'), request.form.get('section_choix'))
        session['candidat']=candidat_en_cours.to_json()
        return render_template('candidat.html',candidat=candidat_en_cours)

    # Si on arrive avec un get et qu'il y a un id_candidat dans la session alors on affiche la liste des sections
    elif request.method == 'GET' and session['candidat']<>'':
        candidat_en_cours=Candidat(session['candidat'])
        return render_template('candidat.html',candidat=candidat_en_cours)

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
        launch_questionnaire = request.form.get('choix_questionnaire')

        return redirect(url_for('question'
                                ,section_en_cours=launch_questionnaire
                                ,id_question='1'))
    else:
        return redirect(url_for('index'))


''' Affichage de la question i de la section choisit '''
@app.route('/question/<string:section_en_cours>/<string:id_question>/', methods=['GET', 'POST'])
def question(section_en_cours,id_question):
    if request.method == 'GET' and session['candidat']<>'':
        # question
        dict_question.get_question(section_en_cours,id_question)

        # search response
        print type(session['candidat'])
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



if __name__ == '__main__':
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run(debug=True, host='0.0.0.0', port=1234)
