# ############### IMPORTATION DES MODULES ET FONCTIONS ######################
# from asyncio import run_coroutine_threadsafe
# from crypt import methods
from cmath import log
import sys
# from turtle import pos
from unicodedata import name
import folium

from sqlalchemy import create_engine
from tabnanny import check
sys.path.append('.')
sys.path.append('..')

from vue import utilisateur
import model,base
from model import *


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

@app.route('/affiche', methods=['POST'])
def affiche():

    n=int(request.form.get('choice_user'))

    fiche = base.session.query(model.User.name, model.User.username, model.User.phone, model.User.email, model.User.address)

    # id = base.session.query(model.User.id)
    # id= base.session.query(model.User.username=='Bret').first()
    # id = model.User.query.filter_by(username = 'Bret').all()
    fiche = base.session.query(model.User.id,model.User.name, model.User.username, model.User.phone, model.User.email)
    k=0
    for el in fiche:
        k+=1
    l = round(k/n)
    if n<k:
        if k>=n:
            return render_template('afiche.html', fiche=fiche, n=n, id=id)

        else:
            try:
                for i in range(k, n):
                    utilisateur(base.f0,i)
                fiche = base.session.query(model.User.name, model.User.username, model.User.phone, model.User.email, model.User.address)
                return render_template('afiche.html', fiche=fiche, n=n, l=l,id=id)
                
            except ConnectionError:
                abort(404)
    else:
        n=5
        fiche = base.session.query(model.User.name, model.User.username, model.User.phone, model.User.email, model.User.address)
        return render_template('afiche.html', fiche=fiche, n=n, l=l)


######## AJOUT DES USERS########

@app.route('/adduser', methods = ('GET', 'POST'))
def adduser():
    if request.method == 'POST':
        cle=base.session.query(model.User.id)
        id=0
        for i in cle:
            id=i['id']
        id+=1
        ajout=model.User(id,request.form['nom'],request.form['prenom'],request.form['tel'],request.form['mail'],request.form['address'], request.form['company'], request.form['site'])
        try:
            base.session.add(ajout)
            base.session.commit()
        finally:
            base.session.close()
            return redirect(url_for('principal'))

    return render_template('adduser.html')

############ MODIFIER USERS ################################
@app.route('/modifierUser/<int:id>', methods=('POST','GET'))
# def recupUser(id):
#     valByIdUser=base.session.query(model.User).filter(model.User.id==id).first()
#     if valByIdUser is None:
#         abort(404)
#     return valByIdUser
# x=recupUser(2)
# print(x.name)
def modifierUser(id):
    user=base.session.query(model.User).filter(model.User.id==id).first()
    if request.method=='POST':
        name = request.form.get('nom')
        username =request.form.get('prenom')
        email=request.form.get('mail')
        address = request.form.get('address')
        phone = request.form.get('tel')
        company = request.form.get('company')
        website = request.form.get('site')
        
        if name is None:
            flash("le nom de l'utilisateur est requis !")
        else:
            user.name=name
            user.username=username
            user.email=email
            user.address=address
            user.phone=phone
            user.company=company
            user.website=website
            base.session.commit()
            return redirect(url_for('principal'))
    return render_template('modifierUser.html', user=user)

#################### SUPPRIMER USERS ################################
@app.route('/supprimerUser/<int:id>', methods=('POST','GET'))
def supprimerUser(id):
    supuser=base.session.query(model.User).filter(model.User.id==id).first()

    # supUser=base.session.query(model.User.id).filter(model.User.id==id).first()
    base.session.delete(supuser)
    base.session.commit()
    base.session.close()
    # for i in supUser:
    #     flash('"{}" a été supprimé avec succès'.format(i['name']))
    return redirect(url_for('principal'))


######################## Page Post ####################################

@app.route('/post')
def post():
    posts=base.session.query(model.Post).all()
    return render_template('post.html', posts=posts)

################### CRÉATION DE POSTS ##############################
@app.route('/createPost', methods=('POST','GET'))
def createPost():
    if request.method == 'POST':
        userId=''
        cle=base.session.query(model.Post.id)
        id=0
        for i in cle:
            id=i['id']
        id+=1
        ajout=model.Post(userId,id,request.form.get('title'),request.form.get('body'))
        try:
            base.session.add(ajout)
            base.session.commit()
        finally:
            base.session.close()
            return redirect(url_for('post'))

    return render_template('addPost.html')
##################### EDITER DES POSTS ##############################
# def recupPost(id):
#     val=base.session.query(model.Post).filter(model.Post.id==id).first()
#     if val is None:
#         abort(404)
#     return val
@app.route('/editerPost/<int:id>', methods=['GET','POST'])
def editerPost(id):
    post=base.session.query(model.Post).filter(model.Post.id==id).first()
    if request.method=='POST':
        titre=request.form.get('title')
        contenu=request.form.get('body')
        Id_util=request.form.get('userId')
        if titre is None:
            flash('le titre est requis!')
        else:
            post.title=titre
            post.body=contenu
            post.userId=Id_util
            post.id=id
            base.session.commit()

            return redirect(url_for('post'))
    return render_template('editerPost.html', post=post)

##################### SUPPRIMER DES POSTS #########################

@app.route('/supprimerPost/<int:id>', methods=('POST','GET'))
def supprimerPost(id):
    suppost=base.session.query(model.Post).filter(model.Post.id==id).first()

    # supp=base.session.query(model.Post.id).filter(model.Post.id==id).first()
    base.session.delete(suppost)
    base.session.commit()
    base.session.close()
    flash("ce post a été supprimé avec succès!")
    return redirect(url_for('post'))


######################## Page Album ####################################

@app.route('/album')
def album():
    albums=base.session.query(model.Album).all()
    return render_template('album.html', albums=albums)


#################### AJOUTER ALBUM #############################
@app.route('/addAlbum', methods=('POST','GET'))
def addAlbum():
    if request.method == 'POST':
        userId=''
        cle=base.session.query(model.Album.id)
        id=0
        for i in cle:
            id=i['id']
        id+=1
        ajout=model.Album(2,id,request.form.get('title'))
        try:
            base.session.add(ajout)
            base.session.commit()
        finally:
            base.session.close()
            return redirect(url_for('album'))

    return render_template('addAlbum.html')

############### MODIFIER ALBUM #########################

@app.route('/modifierAlbum/<int:id>', methods=('GET','POST'))
def modifierAlbum(id):
    album=base.session.query(model.Album).filter(model.Album.id==id).first()
    if request.method=='POST':
        titre=request.form.get('title')
        if titre is None:
            flash('le titre est requis!')
        else:
            # ed0=base.session.query(model.Album.title).filter(model.Album.id==id).first()
            album.title=titre
            # base.session.add(ed0)
            base.session.commit()
            base.session.close()
            return redirect(url_for('album'))
    return render_template('modifierAlbum.html', album=album)



####################### SUPPRIMER ALBUM #############################

@app.route('/supprimerAlbum/<int:id>', methods=('POST','GET'))
def supprimerAlbum(id):
    suppalbum=base.session.query(model.Album).filter(model.Album.id==id).first()
    
    base.session.delete(suppalbum)
    base.session.commit()
    base.session.close()
    # flash('"{}" a été supprimé avec succès!'.format(album.get('title')))
    return redirect(url_for('album'))


######################## Page Photo ####################################

@app.route('/photo')
def photo():
    photos=base.session.query(model.Photo).all()
    return render_template('photo.html', photos=photos)
############################### lien photo #############""


################### AJOUTER DE PHOTO #############################

@app.route('/addPhoto', methods=('POST','GET'))
def addPhoto():
    if request.method == 'POST':
        albumId=''
        # lienPhoto=request.form.get('url')
        cle=base.session.query(model.Photo.id)
        id=0
        for i in cle:
            id=i['id']
        id+=1
        ajout=model.Photo(1,id,request.form.get('title'),request.form.get('url'),request.form.get('thumbnailUrl'))
        try:
            base.session.add(ajout)
            base.session.commit()
        finally:
            base.session.close()
            return redirect(url_for('photo'))

    return render_template('addPhoto.html')


################ MODOFIER PHOTO #########################

@app.route('/modifierPhoto/<int:id>', methods=('GET','POST'))
def modifierPhoto(id):
    photo=base.session.query(model.Photo).filter(model.Photo.id==id).first()
    if request.method=='POST':
        titre=request.form.get('title')
        url=request.form.get('url')
        thum=request.form.get('thumbnailUrl')
        if titre is None:
            flash('le titre est requis!')
        else:
            photo.title=titre
            photo.url=url
            photo.thumbnailUrl=thum
            base.session.commit()
            base.session.close()
            return redirect(url_for('photo'))
    return render_template('modifierPhoto.html', photo=photo)

################ SUPPRIMER PHOTO ##################

@app.route('/supprimerPhoto/<int:id>', methods=('POST','GET'))
def supprimerPhoto(id):
    supphoto=base.session.query(model.Photo).filter(model.Photo.id==id).first()
    
    # suppPhoto=base.session.query(model.Photo.id).filter(model.Photo.id==id).first()
    base.session.delete(supphoto)
    base.session.commit()
    base.session.close()
    # flash('"{}" a été supprimé avec succès!'.format(photo.get('title')))
    return redirect(url_for('photo'))

############### PAGE TODOS ##########################
@app.route('/todo')
def todo():
    todos=base.session.query(model.Todo).all()
    return render_template('todo.html', todos=todos)

################## AJOUTER TODOS ########################

@app.route('/addTodo', methods=('POST','GET'))
def addTodo():
    if request.method == 'POST':
        userId=''
        cle=base.session.query(model.Todo.id)
        id=0
        for i in cle:
            id=i['id']
        id+=1
        ajout=model.Todo(1,id,request.form.get('title'),request.form.get('a_faire'),request.form.get('en_cours'),request.form.get('fini'))
        try:
            base.session.add(ajout)
            base.session.commit()
        finally:
            base.session.close()
            return redirect(url_for('todo'))

    return render_template('addTodo.html')

################## MODIFIER TODOS ##########################

@app.route('/modifierTodo/<int:id>', methods=('GET','POST'))
def modifierTodo(id):
    todo=base.session.query(model.Todo).filter(model.Todo.id==id).first()
    if request.method=='POST':
        titre=request.form.get('title')
        faire=request.form.get('a_faire')
        encours=request.form.get('en_cours')
        fini=request.form.get('fini')
        if titre is None:
            flash('le titre est requis!')
        else:
            todo.title=titre
            todo.a_faire=faire
            todo.en_cours=encours
            todo.fini=fini
            base.session.commit()
            base.session.close()
            return redirect(url_for('todo'))
    return render_template('modifierTodo.html', todo=todo)

################ SUPPRIMER TODOS ##################

@app.route('/supprimerTodo/<int:id>', methods=('POST','GET'))
def supprimerTodo(id):
    suptodo=base.session.query(model.Todo).filter(model.Todo.id==id).first()
    
    # suppTodo=base.session.query(model.Todo.id).filter(model.Todo.id==id).first()
    base.session.delete(suptodo)
    base.session.commit()
    base.session.close()
    # flash('"{}" a été supprimé avec succès!'.format(todo.get('title')))
    return redirect(url_for('todo'))

############### PAGE COMMENTS ##########################
@app.route('/comments')
def comments():
    comments=base.session.query(model.Comment).all()
    return render_template('comments.html', comments=comments)

################ AJOUTER COMMENTS ############################
@app.route('/addComments', methods=('POST','GET'))
def addComments():
    if request.method == 'POST':
        postId=''
        cle=base.session.query(model.Comment.id)
        id=0
        for i in cle:
            id=i['id']
        id+=1
        ajout=model.Comment(1,id,request.form.get('name'),request.form.get('email'),request.form.get('body'))
        try:
            base.session.add(ajout)
            base.session.commit()
        finally:
            base.session.close()
            return redirect(url_for('comments'))

    return render_template('addComments.html')

################## MODOFIER COMMENTS ############################
@app.route('/modifierComments/<int:id>', methods=('GET','POST'))
def modifierComments(id):
    comment=base.session.query(model.Comment).filter(model.Comment.id==id).first()
    if request.method=='POST':
        nom=request.form.get('name')
        mail=request.form.get('email')
        corps=request.form.get('body')
        if nom is None:
            flash('le nom est requis!')
        else:
            comment.name=nom
            comment.email=mail
            comment.body=corps
            base.session.commit()
            base.session.close()
            return redirect(url_for('comments'))
    return render_template('modifierComments.html', comment=comment)

################## SUPPRIMER COMMENTS #######################

@app.route('/supprimerComments/<int:id>', methods=('POST','GET'))
def supprimerComments(id):
    supcomment=base.session.query(model.Comment).filter(model.Comment.id==id).first()
    
    # suppComment=base.session.query(model.Comment.id).filter(model.Comment.id==id).first()
    base.session.delete(supcomment)
    base.session.commit()
    base.session.close()
    # flash('"{}" a été supprimé avec succès!'.format(comment.get('title')))
    return redirect(url_for('comments'))

############ PAGE DE CONNEXION ###########################################
@app.route('/login/', defaults={'email': ""})
@app.route('/login/<email>/<id>', methods=('GET','POST'))
def connexion(email,id):
    if request.method=='POST':
        login=request.form['connect']
        motPass=request.form['secur']
        notfistuser=base.session.query(Connexion.login).filter(Connexion.login==login).first()
        if notfistuser:
            password=base.session.query(Connexion.password).filter(Connexion.login==login).first()
            motPass=password
            return redirect(url_for('userpost'))
            
        else:
            ajoutConnexion=Connexion(login=login, password=motPass,id_user=id)
            base.session.add(ajoutConnexion)
            base.session.commit()
            return redirect(url_for('userpost'))
    return render_template('connexion.html',mail=email,id=id)



########################Page user Post####################################

@app.route('/userpost')
def userpost():
    # post=base.session.query(model.Post).all()
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
   
    return render_template('userinfo.html')


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
    start_coords = (10.9540700, 42.7360300)
    map = folium.Map(
        location=start_coords, 
        zoom_start=2,
        )
    folium.Marker(location=start_coords,
            popup="<i>Marker here</i>",
            tooltip="Click Here").add_to(map)


    company=[namecompany,catchphrase,bs]
    phone = fiche[1]['phone'].split('x')[0]
    lat = float(fiche[1]['address'].split(',')[4].split(':')[-1].strip('}').strip(" ").strip("'"))
    long= float(fiche[1]['address'].split(',')[5].split(':')[-1].strip('}').strip(" ").strip("'"))

    map.save('templates/map.html')
    return render_template('affiche_infos_user.html', fiche=fiche, phone=phone, i=1, company=company, map=map)




# **********************************************************************************

# app.template_folder = 'templates'
# users = list(range(200))
users = base.session.query(model.User.name, model.User.username, model.User.phone, model.User.email, model.User.id).all()


def get_users(offset=0, per_page=5):
    return users[offset: offset + per_page]


@app.route('/paginate', methods=["POST"])
@app.route('/paginate')
def paginate():
    n=(request.form.get('choice_user'))
    a = int(n)
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter= 'per_page')

    total = len(users)
    
    pagination_users = get_users(offset=offset, per_page=per_page)

    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('paginate.html', users=pagination_users, page=page, per_page=5, pagination=pagination, n=n)

# *********************************************************************************

############## DEBOGUER ################################################
if __name__=='__main__':
    app.run(debug=True) 