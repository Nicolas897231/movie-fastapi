from fastapi import FastAPI, Body, Request, HTTPException, Depends, APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from auth import create_token, validate_token
from bd.database import *
from models.users import UserDB


login_user = APIRouter()

class User(BaseModel):
    email:str
    password:str


"""@login_user.post('/login', tags=['Autenticacion'])
def login(user:User):
    if user.email == 'nicolas@mail.com' and user.password == 'as400181':
        token:str = create_token(user.dict())
        print(token)
        return token"""
    

@login_user.post('/login', tags=['Autenticacion'])
def login_user(user:User):
    db = sesion()
    user_login = db.query(UserDB).filter(UserDB.email == user.email).first()
    
    if not user_login:
        return JSONResponse(status_code=404, content={'message':'usuario no existe'})
    
    if user_login.password != user.password:
        return JSONResponse(status_code=404, content={'message':'Contraseña incorrecta'})
    
    token:str = create_token(user.dict())
    return {'token':token, 'messages':'Login Exitoso'}