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
from flask import Blueprint
from flask_paginate import Pagination, get_page_parameter

# *****************************************************************************

from flask import Flask, render_template
from flask_paginate import Pagination, get_page_args

# ****************************************************************************

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

# def get_users(offset=0, per_page=10):
#     return users[offset: offset + per_page]



ligne_par_page = 5

@app.route('/affiche', methods=["POST"])
def affiche(page=2):
    n=int(request.form.get('choice_user'))
    fiche = base.session.query(model.User.name, model.User.username, model.User.phone, model.User.email).all()
    phone = fiche[1]['phone'].split('x')[0]
    page = request.args.get("number")
    # page = request.args.get(get_page_parameter(), type=int, default=1)    
    k=0
    for el in fiche:
        k+=1
    l = round(k/n)

    if k>=5:
        return render_template('afiche.html', fiche=fiche, n=n)

    else:
        try:
            # utilisateur()
            # fiche = base.import_api('users')
            return render_template('afiche.html', fiche=fiche, n=n, l=l)

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
    fiche = base.session.query(model.User.name, model.User.username, model.User.phone, 
    model.User.email, model.User.address).all()
   
    return render_template('userinfo.html'                                                                                                                               )


@app.route('/affiche_infos_user')
def affiche_infos_user():
    fiches = base.import_api('users')
    fiche = base.session.query(model.User.name, model.User.username, model.User.phone, 
    model.User.email, model.User.address).all()
    
    # namecompany = fiches[1]['company'].split(',')[0].split(':')[-1]
    # catchphrase = fiches[1]['company'].split(',')[1].split(':')[-1]
    # bs = fiches[1]['company'].split(',')[2].split(':')[-1]
    
    namecompany = fiches[1]['company']['name']
    catchphrase = fiches[1]['company']['catchPhrase']
    bs = fiches[1]['company']['bs']
    

    company=[namecompany,catchphrase,bs]
    phone = fiche[1]['phone'].split('x')[0]
    lat = float(fiche[1]['address'].split(',')[4].split(':')[-1].strip('}').strip(" ").strip("'"))
    long = float(fiche[1]['address'].split(',')[5].split(':')[-1].strip('}').strip(" ").strip("'"))


    return render_template('affiche_infos_user.html', fiche=fiche, phone=phone, i=1, company=company, lat=lat)


############## DEBOGUER ################################################
if __name__=='__main__':
    app.run(debug=True) 

# **********************************************************************************

app.template_folder = 'templates'
# users = list(range(200))
users = base.session.query(model.User.name, model.User.username, model.User.phone, model.User.email).all()


def get_users(offset=0, per_page=5):
    return users[offset: offset + per_page]


@app.route('/paginate', methods=["POST"])
@app.route('/paginate',)
def paginate():
    n=(request.form.get('choice_user'))
    
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter= 'per_page')

    total = len(users)
    
    pagination_users = get_users(offset=offset, per_page=per_page)

    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('paginate.html', users=pagination_users, page=page, per_page=5, pagination=pagination, n=n)

# *********************************************************************************