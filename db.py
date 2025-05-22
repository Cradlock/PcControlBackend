from sqlalchemy import Column,String,Integer,create_engine,Text,text
from sqlalchemy.orm import create_session,declarative_base,Session
from utils import *
import settings


session : Session = None

Base = declarative_base()






def get_session():
    engine = create_engine(f"postgresql+psycopg2://{settings.USERNAME}:{settings.PASSWORD}@{settings.HOST}:{settings.PORT}/{settings.DMNAME}")
   
    session = create_session(autocommit=False, autoflush=False,bind=engine)
    return session



class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,autoincrement=True)
    username = Column(String,unique=True,nullable=False)
    password = Column(String, nullable=False)
    
    @staticmethod
    def getUser(session : Session,username,password):
        user = session.query(User).filter(User.username == username).first()
        if user:
            if user.password == hashed(password):
                return user 
            return 403
        else:
            return 404
        
    

