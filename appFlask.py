# ############### IMPORTATION DES MODULES ET FONCTIONS ######################
import sys

from vue import utilisateur
sys.path.append('.')
sys.path.append('..')

from flask import Flask, redirect, url_for,render_template,request,flash
import requests
import base,model

#############################################################################

############## APPLICATION FLASK ET SES FONCTIONS DE NAVIGATION #############

app=Flask(__name__)

############# fermeture de session #####################################
# @app.teardown_appcontext
# def stopSession():
#     base.session.remove()

##########################Page Principale ##################################

@app.route('/')
def principal():
    return render_template('principal.html')

################## AFFICHAGE DES USER ######## 

ligne_par_page = 5

@app.route('/affiche', methods=["POST"])
def affiche():
    donnee = request.form
    n = int(donnee.get('choice_user'))

    fiche = base.session.query(model.User.name, model.User.username, model.User.phone, model.User.email)
    request.args.get('page', 1, type = int)
    # fiche.paginate(page, u)

    k=0
    for el in fiche:
        k+=1
    
    if k>=5:
        return render_template('afiche.html', fiche=fiche, n=n)

    else:
        try:
            utilisateur()
            fiche = base.import_api('users')
            return render_template('afiche.html', fiche=fiche, n=n)

        except ConnectionError:
            fiche = "Vous n'etes pas connecter à internet."
                
            return fiche

                ########AJOUT DES USERS########

@app.route('/adduser', methods = ('GET', 'POST'))
def adduser():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        phone = request.form['phone']
        website = request.form['website']
        address = request.form['address']
        ajout=model.User(name,username,phone,website,address)
        base.session.add(ajout)
        base.session.commit()
        redirect(url_for('principal'))

    return render_template('adduser.html')

############ PAGE DE CONNEXION ###########################################
@app.route('/login', methods=('GET','POST'))
def connexion():
    if request.method=='POST':
        mail=request.form['connect']
        motPass=request.form['secur']
        if not mail:
            flash('Ce champ est requis!')
        else:
            redirect(url_for('user'))
    return render_template('connexion.html')

########################Page user Post####################################

@app.route('/userpost')
def userpost():
    return render_template('userpost.html')


########################Page user Album##################################

@app.route('/useralbum')
def useralbum():
    return render_template('useralbum.html')


##########################Page user Todo#################################

@app.route('/usertodo')
def usertodo():
    return render_template('usertodo.html')


#############################Page user Info##############################

@app.route('/userinfo')
def userinfo():
    return render_template('userinfo.html')




############## DEBOGUER ################################################
if __name__=='__main__':
    app.run(debug=True) 

