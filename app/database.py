from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote
from .config import settings

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:%s@localhost/learnfastapi' 

#engine = create_engine(f'postgresql://{settings.database_username}:%s@{settings.database_hostname}/{settings.database_name}' % quote('esak@123'))
engine = create_engine(f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}')

print(f"INFO:: USERNAME ::{settings.database_username}")
print(f"INFO:: PASSWORD ::{settings.database_password}")
print(f"INFO:: HOSTNAME ::{settings.database_hostname}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base() 


# creating Dependency 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()