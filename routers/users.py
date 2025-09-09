from fastapi import FastAPI, Body, Request, HTTPException, Depends, APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from auth import create_token, validate_token
from bd.database import *
from models.movie import Movie as ModelMovie


login_user = APIRouter()

class User(BaseModel):
    email:str
    password:str


@login_user.post('/login', tags=['Autenticacion'])
def login(user:User):
    if user.email == 'nicolas@mail.com' and user.password == 'as400181':
        token:str = create_token(user.dict())
        print(token)
        return token