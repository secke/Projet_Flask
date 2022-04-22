
import sys
sys.path.append('.')
sys.path.append('..')
from sqlalchemy import Boolean, Column,String,Integer,TEXT
import base


class User(base.base):
    __tablename__='users'
    id=Column(Integer, primary_key=True)
    name=Column(String(50))
    username=Column(String(50))
    phone=Column(String(50))
    email=Column(String(100))
    address=Column(String(300))
    
    def __init__(self,id,name,username,phone,email,address):
        self.id=id
        self.name=name
        self.username=username
        self.phone=phone
        self.email=email
        self.address=address
        
        self.email=email
        self.address=address
        
      
        


################## ALBUM #################################

class Album(base.base):
    __tablename__='album'
    userId=Column(Integer)
    id=Column(Integer, primary_key=True)
    title=Column(String(100))
    def __init__(self, userId, id, title):
        self.userId=userId
        self.id=id
        self.title=title

################ PHOTOS #######################################

class Photo(base.base):
    __tablename__='photos'
    albumId=Column(Integer)
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
    userId=Column(Integer)
    id=Column(Integer, primary_key=True)
    title=Column(String(200))
    completed=Column(Boolean)
    def __init__(self,userId, id, title, completed):
        self.userId=userId
        self.id=id
        self.title=title
        self.completed=completed

############## POST ########################

class Post(base.base):
    __tablename__='post'
    userId=Column(Integer)
    id=Column(Integer, primary_key=True)
    title=Column(String(200))
    body=Column(TEXT)
    def __init__(self, userId, id, title, body):
        self.userId=userId
        self.id=id
        self.title=title
        self.body=body



############# COMMENTS ##########################

class Comment(base.base):
    __tablename__='comments'
    postId=Column(Integer)
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





base.init_base()
