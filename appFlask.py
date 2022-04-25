# ############### IMPORTATION DES MODULES ET FONCTIONS ######################
# from asyncio import run_coroutine_threadsafe
# from crypt import methods
from audioop import add
from crypt import methods
import sys
from turtle import pos
from unicodedata import name

from sqlalchemy import create_engine
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

@app.route('/affiche', methods=['POST','GET'])
def affiche():
    n=int(request.form.get('choice_user'))
    fiche = base.session.query(model.User.name, model.User.username, model.User.phone, model.User.email, model.User.address)
    k=0
    for el in fiche:
        k+=1
    if k>=5:
        return render_template('afiche.html', fiche=fiche, n=n)

    else:
        try:
            # utilisateur()
            fiche = base.import_api('users')
            return render_template('afiche.html', fiche=fiche, n=n)

        except ConnectionError:
            fiche = "Vous n'etes pas connecter à internet."

            return fiche


######## AJOUT DES USERS########

@app.route('/adduser', methods = ('GET', 'POST'))
def adduser():
    if request.method == 'POST':
        cle=base.session.query(model.User.id)
        id=0
        for i in cle:
            id=i['id']
        id+=1
        ajout=model.User(id,request.form['nom'],request.form['prenom'],request.form['tel'],request.form['mail'],request.form['address'])
        try:
            base.session.add(ajout)
            base.session.commit()
        finally:
            base.session.close()
            return redirect(url_for('principal'))

    return render_template('adduser.html')

############ MODIFIER USERS ################################
@app.route('/modifierUser/<int:id>', methods=('POST','GET'))
def recupUser(id):
    valByIdUser=base.session.query(model.User).filter(model.User.id==id).first()
    if valByIdUser is None:
        abort(404)
    return valByIdUser
# x=recupUser(2)
# print(x.name)
def modifierUser(id):
    user=recupUser(id)
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
            # ed0=base.session.query(model.User.name).filter(model.User.id==id).first()
            model.User.name=name
            # ed1=base.session.query(model.User.username).filter(model.User.id==id).first()
            model.User.username=username
            model.User.email=email
            # ed4=base.session.query(model.User.address).filter(model.User.id==id).first()
            model.User.address=address
            # ed2=base.session.query(model.User.phone).filter(model.User.id==id).first()
            model.User.phone=phone
            model.User.company=company
            # ed3=base.session.query(model.User.email).filter(model.User.id==id).first()
            model.User.website=website
           
            # base.session.add_all([ed0,ed1,ed2,ed3,ed4])
            base.session.commit()
            return redirect(url_for('principal'))
    return render_template('modifierUser.html', user=user)

#################### SUPPRIMER USERS ################################
@app.route('/supprimerUser/<int:id>', methods=('POST',))
def supprimerUser(id):
    supUser=base.session.query(model.User.id).filter(model.User.id==id).first()
    base.session.delete(supUser)
    base.session.commit()
    base.session.close()
    for i in supUser:
        flash('"{}" a été supprimé avec succès'.format(i['name']))
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
def recupPost(id):
    val=base.session.query(model.Post).filter(model.Post.id==id).first()
    if val is None:
        abort(404)
    return val
@app.route('/editerPost/<int:id>', methods=['GET','POST'])
def editerPost(id):
    post=recupPost(id)
    if request.method=='POST':
        titre=request.form.get('title')
        contenu=request.form.get('body')
        Id_util=request.form.get('userId')
        if titre is None:
            flash('le titre est requis!')
        else:
            # ed0=base.session.query(model.Post.title).filter(model.Post.id==id).first()
            model.Post.title=titre
            # ed1=base.session.query(model.Post.body).filter(model.Post.id==id).first()
            model.Post.body=contenu
            # ed2=base.session.query(model.Post.userId).filter(model.Post.id==id).first()
            model.Post.userId=Id_util
            # ed3=base.session.query(model.Post.id).filter(model.Post.id==id).first()
            model.Post.id=id
            # base.session.add_all([ed2,ed3,ed0,ed1])
            base.session.commit()
            # model.Post.title=title
            # model.Post.body=body
            # model.Post.userId=userId
            # model.Post.id=id
            return redirect(url_for('post'))
    return render_template('editerPost.html', post=post)

##################### SUPPRIMER DES POSTS #########################

@app.route('/supprimerPost/<int:id>', methods=('POST',))
def supprimerPost(id):
    post=recupPost(id)
    supp=base.session.query(model.Post.id).filter(model.Post.id==id).first()
    base.session.delete(supp)
    base.session.commit()
    base.session.close()
    flash('"{}" a été supprimé avec succès!'.format(post.get('title')))
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
        ajout=model.Album(userId,id,request.form.get('title'))
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
            model.Album.title=titre
            # base.session.add(ed0)
            base.session.commit()
            base.session.close()
            return redirect(url_for('album'))
    return render_template('modifierAlbum.html', album=album)



####################### SUPPRIMER ALBUM #############################

@app.route('/supprimerAlbum/<int:id>', methods=('POST',))
def supprimerAlbum(id):
    album=base.session.query(model.Album).filter(model.Post.id==id).first()
    
    suppAlbum=base.session.query(model.Album.id).filter(model.Post.id==id).first()
    base.session.delete(suppAlbum)
    base.session.commit()
    base.session.close()
    flash('"{}" a été supprimé avec succès!'.format(album.get('title')))
    return redirect(url_for('album'))


######################## Page Photo ####################################

@app.route('/photo')
def photo():
    photos=base.session.query(model.Photo).all()
    return render_template('photo.html', photos=photos)

################### AJOUTER DE PHOTO #############################

@app.route('/addPhoto', methods=('POST','GET'))
def addPhoto():
    if request.method == 'POST':
        albumId=''
        cle=base.session.query(model.Photo.id)
        id=0
        for i in cle:
            id=i['id']
        id+=1
        ajout=model.Photo(albumId,id,request.form.get('title'),request.form.get('url'),request.form.get('thumbnailUrl'))
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
            model.Photo.title=titre
            model.Photo.url=url
            model.Photo.thumbnailUrl=thum
            base.session.commit()
            base.session.close()
            return redirect(url_for('photo'))
    return render_template('modifierPhoto.html', photo=photo)

################ SUPPRIMER PHOTO ##################

@app.route('/supprimerPhoto/<int:id>', methods=('POST',))
def supprimerPhoto(id):
    photo=base.session.query(model.Photo).filter(model.Photo.id==id).first()
    
    suppPhoto=base.session.query(model.Photo.id).filter(model.Photo.id==id).first()
    base.session.delete(suppPhoto)
    base.session.commit()
    base.session.close()
    flash('"{}" a été supprimé avec succès!'.format(photo.get('title')))
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
        cle=base.session.query(model.Photo.id)
        id=0
        for i in cle:
            id=i['id']
        id+=1
        ajout=model.Todo(userId,id,request.form.get('title'),request.form.get('a_faire'),request.form.get('en_cours'),request.form.get('fini'))
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
            model.Todo.title=titre
            model.Todo.a_faire=faire
            model.Todo.en_cours=encours
            model.Todo.fini=fini
            base.session.commit()
            base.session.close()
            return redirect(url_for('todo'))
    return render_template('modifierTodo.html', todo=todo)

################ SUPPRIMER TODOS ##################

@app.route('/supprimerTodo/<int:id>', methods=('POST',))
def supprimerTodo(id):
    todo=base.session.query(model.Todo).filter(model.Todo.id==id).first()
    
    suppTodo=base.session.query(model.Todo.id).filter(model.Todo.id==id).first()
    base.session.delete(suppTodo)
    base.session.commit()
    base.session.close()
    flash('"{}" a été supprimé avec succès!'.format(todo.get('title')))
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
        ajout=model.Comment(postId,id,request.form.get('name'),request.form.get('email'),request.form.get('body'))
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
            model.Comment.name=nom
            model.Comment.email=mail
            model.Comment.body=corps
            base.session.commit()
            base.session.close()
            return redirect(url_for('comments'))
    return render_template('modifierComments.html', comment=comment)

################## SUPPRIMER COMMENTS #######################

@app.route('/supprimerComments/<int:id>', methods=('POST',))
def supprimerComments(id):
    comment=base.session.query(model.Comment).filter(model.Comment.id==id).first()
    
    suppComment=base.session.query(model.Comment.id).filter(model.Comment.id==id).first()
    base.session.delete(suppComment)
    base.session.commit()
    base.session.close()
    flash('"{}" a été supprimé avec succès!'.format(comment.get('title')))
    return redirect(url_for('comments'))

############ PAGE DE CONNEXION ###########################################
# @app.route('/login/')
@app.route('/login/<username>', methods=('GET','POST'))
def connexion(username):

    if request.method=='POST':
        mail=request.form['connect']
        motPass=request.form['secur']
        if not mail:
            flash('Ce champ est requis!')
        else:
            redirect(url_for('usertodo'))
    return render_template('connexion.html',us=username)



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
    return render_template('userinfo.html')




############## DEBOGUER ################################################
if __name__=='__main__':
    app.run(debug=True) 

