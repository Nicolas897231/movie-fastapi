from fastapi import FastAPI, Body, Request, HTTPException, Depends, APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from auth import create_token, validate_token
from bd.database import *
from models.movie import Movie as ModelMovie
from routers.movie import routerMovie
from routers.users import login_user

app = FastAPI()
app.include_router(routerMovie)
app.include_router(login_user)

base.metadata.create_all(bind=engine)




@app.get('/')
def read_root():
    return {'Hello': 'World'}



