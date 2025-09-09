from fastapi import FastAPI, Body, Request, HTTPException, Depends, APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional
from auth import create_token, validate_token
from fastapi.security import HTTPBearer
from bd.database import *
from models.movie import Movie as ModelMovie
from fastapi.encoders import jsonable_encoder

routerMovie = APIRouter()



class Movie(BaseModel):
    id: Optional[int] = None
    title:str = Field(min_length=3)
    overview:str
    year:str
    rating:float
    category:str
    
class BrearerJWT(HTTPBearer):
    async def __call__(self, request:Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != 'nicolas@mail.com':
            raise HTTPException(status_code=403, detail='Credenciales Incorrectas') 

@routerMovie.get('/movie/', dependencies=[Depends(BrearerJWT())], tags=['Get Movie'])
def get_movies():
    db = sesion()
    data = db.query(ModelMovie).all()
    return JSONResponse(content=jsonable_encoder(data))


@routerMovie.get('/movies/{id}', tags=['Get Movie'])
def get_movie(id:int):
    db = sesion()
    data = db.query(ModelMovie).filter(ModelMovie.id == id).first()
    if not data:
        return JSONResponse(status_code=404, content={'message':'Recurso no encontrado'})
    return JSONResponse(status_code=200, content=jsonable_encoder(data))

@routerMovie.get('/movies/', tags=['Get Movie'])
def get_movies_category(category:str):
    db = sesion()
    data = db.query(ModelMovie).filter(ModelMovie.category == category).all()
    return JSONResponse(status_code=200, content=jsonable_encoder(data))

@routerMovie.post('/movies', tags=['Get Movie'])
def create_movie(movie:Movie):
    db = sesion()
    newMovie = ModelMovie(**movie.dict())
    db.add(newMovie)
    db.commit()
    return 'ok'

@routerMovie.put('/movies/{id}', tags=['Get Movie'])
def update_movies(id:int, movie:Movie):
    db = sesion()
    data = db.query(ModelMovie).filter(ModelMovie.id == id).first()
    if not data:
        return JSONResponse(status_code=404, content={'messages':'No se encontro el recurso'})
    data.title = movie.title
    data.overview = movie.overview
    data.year = movie.year
    data.rating = movie.rating
    data.category = movie.category
    db.commit()

    return JSONResponse(content={'meesages': 'Se modifico la pelicula'})

@routerMovie.delete('/movies/{id}', tags=['Get Movie'])
def delete_movie(id:int):
    db = sesion()
    data = db.query(ModelMovie).filter(ModelMovie.id == id).first()
    if not data:
        return JSONResponse(status_code=404, content={'messages':'No se encontro el recurso'})
    
    db.delete(data)
    db.commit()
    return JSONResponse(content={'messages':'Se ha eliminado la pelicula', 'data':jsonable_encoder(data)})