import sys
sys.path.append('.')
sys.path.append('..')
from sqlalchemy import Boolean, Column, ForeignKey,String,Integer,TEXT
import base
from sqlalchemy.orm import *


class User(base.base):
    __tablename__='users'
    id=Column(Integer, primary_key=True)
    name=Column(String(50))
    phone=Column(String(50))
    username=Column(String(50))
    email=Column(String(50))
    address=Column(String(400))
    companyName=Column(String(400))
    catchPhrase=Column(String(400))
    companyBs=Column(String(400))
    website=Column(String(300))
    email=Column(String(100))
    address=Column(String(300))
    connexions=relationship("Connexion",back_populates="users")
    
    # def __init__(self,id,name,username,phone,email,address,company):
    # phone=Column(String(50))
    # company=Column(String(300))
    website=Column(String(100))
    # albums=relationship('Album')
    todos=relationship('Todo')
    posts=relationship('Post')
    def __init__(self,id,name,username,phone,email,address, companyName,catchPhrase,companyBs, website):
        self.id=id
        self.name=name
        self.username=username
        self.phone=phone
        self.email=email
        self.address=address
        self.companyName=companyName
        self.catchPhrase=catchPhrase
        self.companyBs=companyBs
        self.website=website
        


################## ALBUM #################################

class Album(base.base):
    __tablename__='album'
    userId=Column(Integer)
    id=Column(Integer, primary_key=True)
    title=Column(String(100))
    photos=relationship("Photo")
    def __init__(self, userId, id, title):
        self.userId=userId
        self.id=id
        self.title=title

################ PHOTOS #######################################

class Photo(base.base):
    __tablename__='photos'
    albumId=Column(Integer, ForeignKey('album.id'))
    id=Column(Integer, primary_key=True)
    title=Column(String(100))
    url=Column(String(200))
    thumbnailUrl=Column(String(200))
    def __init__(self, albumId, id, title, url, thumbnailUrl):
        self.albumId=albumId
        self.id=id
        self.title=title
        self.url=url
        self.thumbnailUrl=thumbnailUrl

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
    comments=relationship("Comment")
    def __init__(self, userId, id, title, body):
        self.userId=userId
        self.id=id
        self.title=title
        self.body=body



############# COMMENTS ##########################

class Comment(base.base):
    __tablename__='comments'
    postId=Column(Integer, ForeignKey('post.id'))
    id=Column(Integer, primary_key=True)
    name=Column(String(100))
    email=Column(String(100))
    body=Column(TEXT)
    def __init__(self, postId, id, name, email, body):
        self.postId=postId
        self.id=id
        self.name=name
        self.email=email
        self.body=body
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

