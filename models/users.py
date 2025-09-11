from bd.database import *
from sqlalchemy import Column, Integer, String, Float

class UserDB(base):
    __tablename__ = "users"
    
    email = Column(String(100), primary_key=True)
    password = Column(String(100))