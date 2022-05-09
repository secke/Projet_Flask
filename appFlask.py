# ############### IMPORTATION DES MODULES ET FONCTIONS ######################
# from asyncio import run_coroutine_threadsafe
# from crypt import methods
# from turtle import pos
from cmath import log
from crypt import methods
import sys
from flask import session
from unicodedata import name
import folium

from sqlalchemy import create_engine
from tabnanny import check
sys.path.append('.')
sys.path.append('..')

from vue import *
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


##########################Page Principale ##################################

@app.route('/',methods=('GET','POST'))
def principal():
    fiche = base.session.query(model.User.name, model.User.username, model.User.phone, model.User.email, model.User.website)
    if request.method=='POST':
            n=int(request.form.get('choice_user'))
            if 'N' not in session:
                session['N'] = n
                # N1=n
            elif n: 
                page=request.args.get('page')
                # session['N'] =0
                session['N'] += n
            print(session)
            nbr_user=len(base.f0)
            N=session['N']
            nbr_page=round(N/5)
            print('nbr:',nbr_user,nbr_page)
            if N<=5:
                deb=0
                fin=N
                test = 0
            else:
                deb=1
                fin=6
                test =1
                if page:
                    deb=(page+1)*page-1
                    if N/page>=page:
                        fin =deb+5
                    else:
                        fin=deb+N%page
            k=0
            for el in fiche:
                k+=1
            if N>k:
                try:
                    nbr_user=len(base.f0)
                    print(nbr_user)
                    if N<nbr_user:
                        for i in range(k, N):
                            utilisateur(base.f0,i)
                    fiche = base.session.query(model.User)
                    return render_template('principal.html',n=n,N=N,deb=deb,fin=fin, test=test,fiche=fiche)
                except (ConnectionError):
                    abort(404)
            elif k>=N:
            
                fiche = base.session.query(model.User).all()
                return render_template('principal.html', N=N,deb=deb,fin=fin, test=test,fiche=fiche, n=n)
    else:
        # if 'N' not in session:
        deb=0
        fin=0
        N=0
        test=0
        if 'N' not in session:
            pass
        else:
            fiche = base.session.query(model.User)
            k=0
            for el in fiche:
                k+=1
            N=session['N']
            nbr_page=round(N/5)
            if N:
                page=(request.args.get('page'))
                if page :
                    page=int(page)
                
                    test =1
                    deb=(page+1)*page-1
                    print('n:',N,page,deb,nbr_page)
                    if N/page>=5:
                        fin =deb+5
                        print(fin)
                    else:
                        rest=N-deb
                        fin= N
                    print('n:',N,page,deb,fin,k)
            print(fiche)
        return render_template('principal.html',deb=deb,fin=fin,fiche=fiche, N=N,test=test)



######## AJOUT DES USERS########

@app.route('/adduser', methods = ('GET', 'POST'))
def adduser():
    if request.method == 'POST':
        cle=base.session.query(model.User.id).all()
        liste=[]
        for i in cle:
            liste.append(i['id'])
        m=max(liste)
        id=m+1
        ajout=model.User(id,request.form['nom'],request.form['prenom'],request.form['mail'],request.form['street'],request.form['suite'],
        request.form['city'],request.form['zipcode'],request.form['lat'],request.form['lng'],request.form['tel'],request.form['site'],
        request.form['companyName'],request.form['catchphrase'],request.form['bs'],1)
        try:
            base.session.add(ajout)
            base.session.commit()
        finally:
            base.session.close()
            return redirect(url_for('principal'))

    return render_template('adduser.html')

############ MODIFIER USERS ################################
@app.route('/modifierUser/<int:id>', methods=('POST','GET'))
def modifierUser(id):
    user=base.session.query(model.User).filter(model.User.id==id).first()
    # print(user)
    if request.method=='POST':
        name = request.form.get('nom')
        username =request.form.get('prenom')
        email=request.form.get('mail')
        street=request.form.get('street')
        suite=request.form.get('suite')
        city=request.form.get('city')
        zipcode=request.form.get('zipcode')
        lat=request.form.get('lat')
        lng=request.form.get('lng')
        phone = request.form.get('tel')
        website = request.form.get('site')
        companyName = request.form.get('companyName')
        catchPhrase=request.form.get('catchPhrase')
        bs=request.form.get('bs')
        
        
        if name is None:
            flash("le nom de l'utilisateur est requis !")
        else:
            user.name=name
            user.username=username
            user.email=email
            user.street=street
            user.suite=suite
            user.city=city
            user.zipcode=zipcode
            user.lat=lat
            user.lng=lng
            user.phone=phone
            user.website=website
            user.companyName=companyName
            user.catchPhrase=catchPhrase
            user.companyBs=bs
            base.session.commit()
            flash(f"l'utilisateur {name} a été modifié avec succès !")
            return redirect(url_for('principal'))
    return render_template('modifierUser.html', user=user)

#################### SUPPRIMER USERS ################################
@app.route('/supprimerUser/<int:id>', methods=('POST','GET'))
def supprimerUser(id):
    supuser=base.session.query(model.User).filter(model.User.id==id).first()
    # archUser=base.session.query(model.User).filter(model.User.id==id).first()
    supuser.etat=0
    flash(f"l'utilisateur {supuser.name} a été supprimé avec succès !")
    
    # supUser=base.session.query(model.User.id).filter(model.User.id==id).first()
    # base.session.delete(supuser)
    base.session.commit()
    base.session.close()
    

    return redirect(url_for('principal'))


######################## Page Post ####################################

@app.route('/post/<int:userId>')
def post(userId):
    # posts=base.session.query(model.Post).all()
    postsUser=base.session.query(model.Post).filter(model.Post.userId==userId).filter(model.Post.etat==1).all()
    
    if postsUser:
        postUserId=base.session.query(model.Post.id).filter(model.Post.userId==userId).first()
        postId=postUserId[0]
        return render_template('post.html',userId=userId,postsUser=postsUser,postId=2)
    else:
        donnees_post(userId)
        # postId=donnees_post(userId)
        postsUser=base.session.query(model.Post).filter(model.Post.userId==userId).filter(model.Post.etat==1).all()
        postUserId=base.session.query(model.Post.id).filter(model.Post.userId==userId).first()
        # postId=postUserId['id']
        # postsUserApi=base.session.query(model.Post).filter(model.Post.userId==userId).all()
        return render_template('post.html',userId=userId,postsUser=postsUser,postId=postId)
    # return render_template('post.html', posts=posts,userId=userId)

################### CRÉATION DE POSTS ##############################
@app.route('/createPost/<int:userId>', methods=('POST','GET'))
def createPost(userId):
    if request.method == 'POST':
        
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
            return redirect(url_for('post',userId=userId))

    return render_template('addPost.html',userId=userId)
##################### EDITER DES POSTS ##############################
# def recupPost(id):
#     val=base.session.query(model.Post).filter(model.Post.id==id).first()
#     if val is None:
#         abort(404)
#     return val
@app.route('/editerPost/<int:id>/<int:userId>', methods=['GET','POST'])
def editerPost(id,userId):
    post=base.session.query(model.Post).filter(model.Post.id==id).first()
    if request.method=='POST':
        titre=request.form.get('title')
        contenu=request.form.get('body')
        Id_util=request.form.get('userId')
        if not titre:
            flash('le titre est requis!')
        else:
            post.title=titre
            post.body=contenu
            post.userId=Id_util
            post.id=id
            base.session.commit()
            # , post=post,userId=userId
            return redirect(url_for('post',post=post,userId=userId))
    return render_template('editerPost.html',post=post,userId=userId)

##################### SUPPRIMER DES POSTS #########################

@app.route('/supprimerPost/<int:id>/<int:userId>', methods=('POST','GET'))
def supprimerPost(id,userId):
    suppost=base.session.query(model.Post).filter(model.Post.id==id).first()
    # archUser=base.session.query(model.User).filter(model.User.id==id).first()
    suppost.etat=0
    flash(f"le post {suppost.id} a été supprimé avec succès!")
    # supp=base.session.query(model.Post.id).filter(model.Post.id==id).first()
    # base.session.delete(suppost)
    base.session.commit()
    base.session.close()
    return redirect(url_for('post',userId=userId))


######################## Page Album ####################################

@app.route('/album/<int:userId>')
def album(userId):
    # albums=base.session.query(model.Album).all()
    albumsUser=base.session.query(model.Album).filter(model.Album.userId==userId).filter(model.Album.etat==1).all()
    
    if albumsUser:
        albumUserId=base.session.query(model.Album.id).filter(model.Album.userId==userId).first()
        albumId=albumUserId[0]
        return render_template('album.html',userId=userId,albumsUser=albumsUser,albumId=albumId)
    else:
        donnees_album(userId)
        # albumId=donnees_album(userId)
        albumsUser=base.session.query(model.Album).filter(model.Album.userId==userId).filter(model.Album.etat==1).all()
        albumUserId=base.session.query(model.Album.id).filter(model.Album.userId==userId).first()
        albumId=albumUserId[0]
        # albumsUserApi=base.session.query(model.Post).filter(model.Post.userId==userId).all()
        return render_template('album.html',userId=userId,albumsUser=albumsUser,albumId=albumId)
    # return render_template('album.html', albums=albums,userId=userId)


#################### AJOUTER ALBUM #############################
@app.route('/addAlbum/<int:userId>', methods=('POST','GET'))
def addAlbum(userId):
    if request.method == 'POST':
        
        cle=base.session.query(model.Album.id).all()
        liste=[]
        for i in cle:
            liste.append(i['id'])
        m=max(liste)
        id=m+1
        ajout=model.Album(userId,id,request.form.get('title'))
        try:
            base.session.add(ajout)
            base.session.commit()
        finally:
            base.session.close()
            return redirect(url_for('album',userId=userId))

    return render_template('addAlbum.html',userId=userId)

############### MODIFIER ALBUM #########################

@app.route('/modifierAlbum/<int:id>/<int:userId>', methods=('GET','POST'))
def modifierAlbum(id,userId):
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
            return redirect(url_for('album',userId=userId))
    return render_template('modifierAlbum.html', album=album,userId=userId)



####################### SUPPRIMER ALBUM #############################

@app.route('/supprimerAlbum/<int:id>/<int:userId>', methods=('POST','GET'))
def supprimerAlbum(id,userId):
    suppalbum=base.session.query(model.Album).filter(model.Album.id==id).first()
    # archUser=base.session.query(model.User).filter(model.User.id==id).first()
    suppalbum.etat=0
    flash(f"L'album {suppalbum.title} a été supprimé avec succès!")

    # base.session.delete(suppalbum)
    base.session.commit()
    base.session.close()
    return redirect(url_for('album',userId=userId))


######################## Page Photo ####################################

@app.route('/photo/<int:albumId>', methods=['POST','GET'])
def photo(albumId):
    # photos=base.session.query(model.Photo).all()
    photosAlbum=base.session.query(model.Photo).filter(model.Photo.albumId==albumId).filter(model.Photo.etat==1).all()
    # commentalbumId=base.session.query(model.Comment.id).filter(model.Comment.albumId==albumId).first()
    if photosAlbum:
        return render_template('photo.html',photosAlbum=photosAlbum,albumId=albumId)
    else:
        donnees_photo(albumId)
        photosAlbum=base.session.query(model.Photo).filter(model.Photo.albumId==albumId).filter(model.Photo.etat==1).all()
        return render_template('photo.html',photosAlbum=photosAlbum,albumId=albumId)
    # return render_template('photo.html', photos=photos,albumId=albumId)
############################### lien photo #############""


################### AJOUTER DE PHOTO #############################

@app.route('/addPhoto/<int:albumId>', methods=('POST','GET'))
def addPhoto(albumId):
    if request.method == 'POST':
        # lienPhoto=request.form.get('url')
        cle=base.session.query(model.Photo.id).all()
        liste=[]
        for i in cle:
            liste.append(i['id'])
        m=max(liste)
        id=m+1
        ajout=model.Photo(albumId,id,request.form.get('title'),request.form.get('url'),request.form.get('thumbnailUrl'))
        try:
            base.session.add(ajout)
            base.session.commit()
        finally:
            base.session.close()
            return redirect(url_for('photo',albumId=albumId))

    return render_template('addPhoto.html',albumId=albumId)


################ MODOFIER PHOTO #########################

@app.route('/modifierPhoto/<int:id>/<int:albumId>', methods=('GET','POST'))
def modifierPhoto(id,albumId):
    photo=base.session.query(model.Photo).filter(model.Photo.id==id).first()
    if request.method=='POST':
        titre=request.form.get('title')
        url=request.form.get('url')
        thum=request.form.get('thumbnailUrl')
        if not titre:
            flash('le titre est requis!')
        else:
            photo.id = id
            photo.title=titre
            photo.url=url
            photo.thumbnailUrl=thum
            base.session.commit()
            base.session.close()
            return redirect(url_for('photo',albumId=albumId))
    return render_template('modifierPhoto.html', photo=photo,albumId=albumId)

################ SUPPRIMER PHOTO ##################

@app.route('/supprimerPhoto/<int:id>/<int:albumId>', methods=('POST','GET'))
def supprimerPhoto(id,albumId):
    supphoto=base.session.query(model.Photo).filter(model.Photo.id==id).first()
    # archUser=base.session.query(model.User).filter(model.User.id==id).first()
    supphoto.etat=0
    flash(f"La photo {supphoto.title} a été supprimé avec succès!")

    # suppPhoto=base.session.query(model.Photo.id).filter(model.Photo.id==id).first()
    # base.session.delete(supphoto)
    base.session.commit()
    base.session.close()
    return redirect(url_for('photo',albumId=albumId))

############### PAGE TODOS ##########################
@app.route('/todo/<int:userId>')
def todo(userId):
    todos=base.session.query(model.Todo).filter(model.Todo.userId==userId).all()
    taille=len(todos)
    if todos:
        todosUserId=base.session.query(model.Todo).filter(model.Todo.userId==userId).first()
        return render_template('todo.html',todos=todos,userId=userId,taille=taille)
    else:
        print(userId)
        donnees_todo(userId)
        todos=base.session.query(model.Todo).filter(model.Todo.userId==userId).all()
        todosUserId=base.session.query(model.Todo).filter(model.Todo.userId==userId).first()
        # todosId=todosUserId[0]
        return render_template('todo.html',todos=todos,userId=userId,taille=taille)

################## AJOUTER TODOS ########################
@app.route('/addTodo/<int:userId>', methods=('POST','GET'))
def addTodo(userId):
    if request.method == 'POST':
        
        cle=base.session.query(model.Todo.id).all()
        liste=[]
        for i in cle:
            liste.append(i['id'])
        m=max(liste)
        id=m+1
        ajout=model.Todo(userId,id,request.form.get('title'),request.form.get('ETAT'))
        try:
            base.session.add(ajout)
            base.session.commit()
        finally:
            base.session.close()
            return redirect(url_for('todo',userId=userId))

    return render_template('addTodo.html',userId=userId)

################## MODIFIER TODOS ##########################

@app.route('/modifierTodo/<int:id>/<int:userId>', methods=('GET','POST'))
def modifierTodo(id,userId):
    todo=base.session.query(model.Todo).filter(model.Todo.id==id).first()
    if request.method=='POST':
        titre=request.form.get('title')
        ETAT=request.form.get('ETAT')
        if titre is None:
            flash('le titre est requis!')
        else:
            todo.title=titre
            todo.ETAT=ETAT
            base.session.commit()
            base.session.close()
            return redirect(url_for('todo',userId=userId))
    return render_template('modifierTodo.html', todo=todo,userId=userId)

################ SUPPRIMER TODOS ##################

@app.route('/supprimerTodo/<int:id>/<int:userId>', methods=('POST','GET'))
def supprimerTodo(id,userId):
    suptodo=base.session.query(model.Todo).filter(model.Todo.id==id).first()
    
    # suppTodo=base.session.query(model.Todo.id).filter(model.Todo.id==id).first()
    base.session.delete(suptodo)
    base.session.commit()
    base.session.close()
    # flash('"{}" a été supprimé avec succès!'.format(todo.get('title')))
    return redirect(url_for('todo',userId=userId))

############### PAGE COMMENTS ##########################
@app.route('/comments/<int:postId>')
def comments(postId):
    commentsPost=base.session.query(model.Comment).filter(model.Comment.postId==postId).filter(model.Comment.etat==1).all()
    # commentPostId=base.session.query(model.Comment.id).filter(model.Comment.postId==postId).first()
    if commentsPost:
        return render_template('comments.html',commentsPost=commentsPost,postId=postId)
    else:
        donnees_comment(postId)
        commentsPost=base.session.query(model.Comment).filter(model.Comment.postId==postId).filter(model.Comment.etat==1).all()
        return render_template('comments.html',commentsPost=commentsPost,postId=postId)

    # return render_template('comments.html', comments=comments,postId=postId)

################ AJOUTER COMMENTS ############################
@app.route('/addComments/<int:postId>', methods=('POST','GET'))
def addComments(postId):
    if request.method == 'POST':
        # postId=''
        cle=base.session.query(model.Comment.id).all()
        liste=[]
        for i in cle:
            liste.append(i['id'])
        m=max(liste)
        id=m+1
        ajout=model.Comment(postId,id,request.form.get('name'),request.form.get('email'),request.form.get('body'))
        try:
            base.session.add(ajout)
            base.session.commit()
        finally:
            base.session.close()
            return redirect(url_for('comments',postId=postId))

    return render_template('addComments.html',postId=postId)

################## MODOFIER COMMENTS ############################
@app.route('/modifierComments/<int:id>/<int:postId>', methods=('GET','POST'))
def modifierComments(id,postId):
    comment=base.session.query(model.Comment).filter(model.Comment.id==id).first()
    if request.method=='POST':
        nom=request.form.get('name')
        mail=request.form.get('email')
        corps=request.form.get('body')
        if not nom:
            flash('le nom est requis!')
        else:
            comment.name=nom
            comment.email=mail
            comment.body=corps
            base.session.commit()
            flash(f"le commentaire {comment.id} a été modifié avec succès!")
            base.session.close()
            return redirect(url_for('comments',postId=postId))
    return render_template('modifierComments.html', comment=comment,postId=postId)

################## SUPPRIMER COMMENTS #######################

@app.route('/supprimerComments/<int:id>/<int:postId>', methods=('POST','GET'))
def supprimerComments(id,postId):
    supcomment=base.session.query(model.Comment).filter(model.Comment.id==id).first()
    # archUser=base.session.query(model.User).filter(model.User.id==id).first()
    supcomment.etat=0
    flash(f"le commentaire {supcomment.id} a été supprimé avec succès!")
    # suppComment=base.session.query(model.Comment.id).filter(model.Comment.id==id).first()
    # base.session.delete(supcomment)
    base.session.commit()
    base.session.close()
    return redirect(url_for('comments',postId=postId))

############ PAGE DE CONNEXION ###########################################
@app.route('/login/', defaults={'email': ""})
@app.route('/login/<email>/<id>', methods=('GET','POST'))
def connexion(email,id):

    if request.method=='POST':
        login=request.form['connect']
        userConnect=request.form['connect']
        session['email']=userConnect
        userId=base.session.query(model.User.id).filter(model.User.email==login).first()[0]
        name=base.session.query(model.User.name).filter(model.User.id==userId).first()[0]
        motPass=request.form['secur']
        print("motPass:",motPass)
        notfistuser=base.session.query(Connexion.login).filter(Connexion.login==login).first()
        print("username:",notfistuser)
        if notfistuser:
            password=base.session.query(Connexion.password).filter(Connexion.login==login).first()[0]
            print("password:",password)
            if motPass==password:
                print("OOOOKKKK")
                return redirect(url_for('userpost',userId=userId, name=name))
            
        else:
            ajoutConnexion=Connexion(login=login, password=motPass,id_user=id)
            base.session.add(ajoutConnexion)
            base.session.commit()
            return redirect(url_for('userpost',userId=userId,name=name))
    return render_template('connexion.html',mail=email,id=id)

######################### PAGE DE DÉCONNEXION ################################

@app.route('/deconnexion')
def deconnexion():
    session.pop('email',None)
    flash("UTILISATEUR DÉCONNECTÉ AVEC SUCCÈS!")
    # if 'email' in session:
    #     print('OK')
    # else:
    #     print('OOPS')
    return redirect(url_for('principal'))



########################Page user Post####################################

@app.route('/userpost/<int:userId>/<name>')
def userpost(userId,name):
    #   
    # post=base.session.query(model.Post).all()
    return render_template('userpost.html',userId=userId,name=name)



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
    model.User.email, model.User.street).all()
   
    return render_template('userinfo.html')


@app.route('/affiche_infos_user/<int:userId>')
def affiche_infos_user(userId):
    # print(userId)
    # fiches = base.import_api('users')
    fiche = base.session.query(model.User.name, model.User.username, model.User.phone, 
    model.User.email, model.User.city,model.User.lat, 
    model.User.lng,model.User.companyName,model.User.catchPhrase,model.User.companyBs).filter(model.User.id==userId).first()
    
    # namecompany = fiche['company'].split(',')[0].split(':')[-1].strip(' ').strip("'")
    # catchphrase = fiche['company'].split(',')[1].split(':')[-1].strip(' ').strip("'")
    # bs = fiche['company'].split(',')[2].split(':')[-1].split('}')[0].strip(' ').strip("'")
    
    phone = fiche['phone'].split('x')[0]
    lat=fiche['lat']
    long=fiche['lng']
    # lat = float(fiche['address'].split(',')[4].split(':')[-1].strip('}').strip(" ").strip("'"))
    # long= float(fiche['address'].split(',')[5].split(':')[-1].strip('}').strip(" ").strip("'"))
    # rue= fiche['address'].split(',')[1].split(':')[1].strip('"')
    # ville= fiche['address'].split(',')[2].split(':')[1].strip('"').strip(' ').strip("'")
    # rue=fiche['street']
    # ville=fiche['city']
    start_coords = (lat, long)
    map = folium.Map(
        location=start_coords, 
        zoom_start=2,
        )
    folium.Marker(location=start_coords,
            popup="<i>Marker here</i>",
            tooltip="Click Here").add_to(map)

    map.save('templates/map.html')
    return render_template('affiche_infos_user.html', fiche=fiche, phone=phone, i=1, map=map,userId=userId)




##########################" PAGE DE PAGINATION ##################################"

# app.template_folder = 'templates'
# users = list(range(200))
users = base.session.query(model.User.name, model.User.username, model.User.phone, model.User.email, model.User.id).all()


def get_users(offset=0, per_page=5):
    return users[offset: offset + per_page]


@app.route('/paginate', methods=["POST","GET"])
@app.route('/paginate')
def paginate():
    n=request.form.get('choice_user')
    a = int(n)
#### J'ai modifié beaucoup de choses ici (importation d'éléments depuis la fonction "affiche")###

    fiche = base.session.query(model.User.name, model.User.username, model.User.phone, model.User.email, model.User.address)
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter= 'per_page')

    total = len(users)
    l=round(total/a)
    userId=base.session.query(model.User.id).filter(model.User.email=='Bret').first()
    pagination_users = get_users(offset=offset, per_page=per_page)

    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')
    k=0
    for el in fiche:
        k+=1
    # l = round(k/n)
    if a>k:
        if k>=a:
            return render_template('paginate.html', users=pagination_users, page=page, per_page=5, pagination=pagination, a=a,l=l,userId=userId)

        else:
            try:
                for i in range(k, a):
                    utilisateur(base.f0,i)
                fiche = base.session.query(model.User.name, model.User.username, model.User.phone, model.User.email, model.User.address)
                return render_template('paginate.html', users=pagination_users, page=page, per_page=5, pagination=pagination, a=a,l=l,userId=userId)
                
            except ConnectionError:
                abort(404)
    else:
        a=5
        fiche = base.session.query(model.User.name, model.User.username, model.User.phone, model.User.email, model.User.address)
        return render_template('paginate.html', users=pagination_users, page=page, per_page=5, pagination=pagination, a=a,l=l,userId=userId)


    # return render_template('paginate.html', users=pagination_users, page=page, per_page=5, pagination=pagination, a=a,l=l,userId=userId)

# *********************************************************************************

############## DEBOGUER ################################################
if __name__=='__main__':
    app.run(debug=True) 