# ############### IMPORTATION DES MODULES ET FONCTIONS ######################
# from asyncio import run_coroutine_threadsafe
# from crypt import methods
import sys
sys.path.append('.')
sys.path.append('..')

from vue import utilisateur
import model,base


from flask import Flask, redirect, url_for,render_template,request,flash
import requests
import werkzeug
from werkzeug.exceptions import abort


########################################################################

############## APPLICATION FLASK ET SES FONCTIONS DE NAVIGATION #############

app=Flask(__name__)

app.config['SECRET_KEY']='Groupe_7_2022'
############# fermeture de session #####################################
# @app.teardown_appcontext
# def stopSession():
#     base.session.remove()

##########################Page Principale ##################################

@app.route('/')
def principal():
    return render_template('principal.html')

################## AFFICHAGE DES USER ######## 

@app.route('/affiche', methods=["POST"])
def affiche():
    n=int(request.form.get('choice_user'))
    fiche = base.session.query(model.User.name, model.User.username, model.User.phone, model.User.email)
    k=0
    val_login=request
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


######## AJOUT DES USERS########

@app.route('/adduser', methods = ('GET', 'POST'))
def adduser():
    if request.method == 'POST':
        # name = 
        # username = 
        # phone = 
        # website = 
        # address = request.form['address']
        ajout=model.User(request.form['nom'],request.form['prenom'],request.form['tel'],request.form['site'])
        base.session.add(ajout)
        base.session.commit()
        redirect(url_for('principal'))

    return render_template('adduser.html')

##################### EDITER DES POSTS ##############################
def recupPost(id):
    val=base.session.query(model.Post.id).first()
    if val is None:
        abort(404)
    return val
@app.route('/<int:id>/editer', methods=['GET','POST'])
def editer(id):
    post=recupPost(id)
    if request.method=='POST':
        titre=request.form.get('title')
        contenu=request.form.get('body')
        Id_util=request.form.get('userId')
        if titre is None:
            flash('le titre est requis!')
        else:
            ed0=base.session.query(model.Post.title).filter(model.Post.id==id).first()
            ed0=titre
            ed1=base.session.query(model.Post.body).filter(model.Post.id==id).first()
            ed1=contenu
            ed2=base.session.query(model.Post.userId).filter(model.Post.id==id).first()
            ed2=Id_util
            ed3=base.session.query(model.Post.id).filter(model.Post.id==id).first()
            ed3=id
            base.session.add_all([ed2,ed3,ed0,ed1])
            base.session.commit()
            # model.Post.title=title
            # model.Post.body=body
            # model.Post.userId=userId
            # model.Post.id=id
            return redirect(url_for('principal'))
    return render_template('editer.html', post=post)

##################### SUPPRIMER DES POSTS #########################

@app.route('/<int:id>/supprimer', methods=('POST',))
def suppression(id):
    post=recupPost(id)
    supp=base.session.query(model.Post).filter(model.Post.id==id)
    base.session.delete(supp)
    base.commit()
    flash('"{}" a été supprimé avec succès!'.format(post.get('title')))
    return redirect(url_for('principal'))




############ PAGE DE CONNEXION ###########################################
@app.route('/login/', methods=('GET','POST'))
def connexion():

    if request.method=='POST':
        mail=request.form['connect']
        motPass=request.form['secur']
        if not mail:
            flash('Ce champ est requis!')
        else:
            redirect(url_for('usertodo'))
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

