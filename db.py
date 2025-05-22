from sqlalchemy import Column,String,Integer,create_engine,Text,text
from sqlalchemy.orm import create_session,declarative_base,Session,sessionmaker
from utils import *
import settings



Base = declarative_base()



SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{settings.USERNAME}:{settings.PASSWORD}@{settings.HOST}:{settings.PORT}/{settings.DMNAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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
        
    

