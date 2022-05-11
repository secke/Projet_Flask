import sys
from folium import ColorLine
sys.path.append('.')
sys.path.append('..')
from sqlalchemy import Boolean, Column, ForeignKey,String,Integer,TEXT
import base
from sqlalchemy.orm import *


class User(base.base):
    __tablename__='users'
    id=Column(Integer, primary_key=True)
    name=Column(String(50))
    username=Column(String(50))
    email=Column(String(50))
    street=Column(String(200))
    suite=Column(String(200))
    city=Column(String(200))
    zipcode=Column(String(200))
    lat=Column(String(50))
    lng=Column(String(50))
    phone=Column(String(50))
    website=Column(String(100))
    companyName=Column(String(400))
    catchPhrase=Column(String(400))
    companyBs=Column(String(400))
    etat=Column(Integer)
    connexions=relationship("Connexion",back_populates="users")
    # albums=relationship('Album')
    todos=relationship('Todo')
    posts=relationship('Post')
    def __init__(self,id,name,username,email,street,suite,city,zipcode,lat,lng,
    phone, website, companyName,catchPhrase,companyBs,etat):
        self.id=id
        self.name=name
        self.username=username
        self.email=email
        self.street=street
        self.suite=suite
        self.city=city
        self.zipcode=zipcode
        self.lat=lat
        self.lng=lng
        self.phone=phone
        self.website=website
        self.companyName=companyName
        self.catchPhrase=catchPhrase
        self.companyBs=companyBs
        self.etat=etat
        


################## ALBUM #################################

class Album(base.base):
    __tablename__='album'
    userId=Column(Integer)
    id=Column(Integer, primary_key=True)
    title=Column(String(100))
    etat=Column(Integer)
    photos=relationship("Photo")
    def __init__(self, userId, id, title,etat):
        self.userId=userId
        self.id=id
        self.title=title
        self.etat=etat

################ PHOTOS #######################################

class Photo(base.base):
    __tablename__='photos'
    albumId=Column(Integer, ForeignKey('album.id'))
    id=Column(Integer, primary_key=True)
    title=Column(String(100))
    url=Column(String(200))
    thumbnailUrl=Column(String(200))
    etat=Column(Integer)
    def __init__(self, albumId, id, title, url, thumbnailUrl,etat):
        self.albumId=albumId
        self.id=id
        self.title=title
        self.url=url
        self.thumbnailUrl=thumbnailUrl
        self.etat=etat

############## TODOS ##############################

class Todo(base.base):
    __tablename__='todo'
    userId=Column(Integer, ForeignKey('users.id'))
    id=Column(Integer, primary_key=True)
    title=Column(String(200))
    ETAT=Column(TEXT)
    
    # completed=Column(Boolean)
    def __init__(self,userId, id, title, ETAT):
        self.userId=userId
        self.id=id
        self.title=title
        self.ETAT=ETAT

############## POST ########################

class Post(base.base):
    __tablename__='post'
    userId=Column(Integer, ForeignKey('users.id'))
    id=Column(Integer, primary_key=True)
    title=Column(String(200))
    body=Column(TEXT)
    etat=Column(Integer)
    comments=relationship("Comment")
    def __init__(self, userId, id, title, body,etat):
        self.userId=userId
        self.id=id
        self.title=title
        self.body=body
        self.etat=etat



############# COMMENTS ##########################

class Comment(base.base):
    __tablename__='comments'
    postId=Column(Integer, ForeignKey('post.id'))
    id=Column(Integer, primary_key=True)
    name=Column(String(100))
    email=Column(String(100))
    body=Column(TEXT)
    etat=Column(Integer)
    def __init__(self, postId, id, name, email, body,etat):
        self.postId=postId
        self.id=id
        self.name=name
        self.email=email
        self.body=body
        self.etat=etat
        # self.password=password


############Connexion############################

class Connexion(base.base):
    __tablename__='connexions'
    id=Column(Integer, primary_key=True,autoincrement=True)
    login=Column(String(50))
    password=Column(String(50))
    id_user=Column(Integer,ForeignKey('users.id')) 
    users=relationship("User",back_populates="connexions")

    def __init__(self ,login,password,id_user):
        self.login=login
        self.password=password
        self.id_user=id_user





# print(model.User.query.all())


base.init_base()

