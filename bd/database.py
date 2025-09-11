import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DATABASE_URL = "mysql+pymysql://root:as400181@18.221.119.50:3306/movies"


engine = create_engine(DATABASE_URL, echo=True)

sesion = sessionmaker(bind=engine)

base = declarative_base()