################# BASE DE DONNÉES #################################################
import sys
sys.path.append('.')
sys.path.append('..')
from sqlalchemy import create_engine,Column,String,Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import requests 



#engine=create_engine('postgresql://secke:keita2022@localhost:5432/baseflask')
engine=create_engine('postgresql://groupe7:test_123@localhost:5432/flask_db')
base_session=sessionmaker(bind=engine,autocommit=False,autoflush=False)
session=base_session()
base=declarative_base()
# base.query=base_session.query_property()
def init_base():
    # import model
    base.metadata.create_all(bind=engine)

def import_api(x):
    Lien0="https://jsonplaceholder.typicode.com/"
    Lien1=Lien0+x
    f=requests.get(Lien1)
    fichier=f.json()
    return fichier

f0=import_api('users')

f1=import_api('albums')

f2=import_api('photos')

f3=import_api('todos')

f4=import_api('posts')

f5=import_api('comments')







# u=User(1,'lamine','Lamzo09')
# session.add(u)
# session.commit()
