from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

# add you mysql username nad password 
engine=create_engine("mysql://username:password@localhost:3306/fastapi")

meta= MetaData()
conection=engine.connect()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
