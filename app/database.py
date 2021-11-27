from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote  

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:%s@localhost/learnfastapi' 

engine = create_engine('postgresql://postgres:%s@localhost/learnfastapi' % quote('esak@123'))

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base() 


# creating Dependency 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()