################# BASE DE DONNÉES #################################################
import sys
sys.path.append('.')
sys.path.append('..')
from sqlalchemy import create_engine,Column,String,Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base



engine=create_engine('postgresql://secke:keita2022@localhost:5432/baseflask')
engine=create_engine('postgresql://groupe7:test_123@localhost:5432/flask_db')
base_session=sessionmaker(bind=engine,autocommit=False,autoflush=False)
session=base_session()
base=declarative_base()
# base.query=base_session.query_property()
def init_base():
    # import model
    base.metadata.create_all(bind=engine)






# u=User(1,'lamine','Lamzo09')
# session.add(u)
# session.commit()
