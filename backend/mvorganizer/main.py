from http.client import responses
from unicodedata import category
from fastapi import FastAPI
from . import schemas
from .utils import list_files

from .config import get_config
from .models import Base
from .base_db import engine
from fastapi import Depends, FastAPI, status
from fastapi.exceptions import HTTPException
from os.path import splitext
from .session import get_db
from .base_db import Session
from . import crud
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware

config = get_config()

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https?://(?:127\.0\.0\.1|localhost):300[0-9]",
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def hello():
    return "Hello from FastAPI"


@app.get("/movies", response_model=List[schemas.MovieFile])
def get_all_movies(db: Session = Depends(get_db)):
    return crud.get_all_movies(db)


@app.post(
    "/movies",
    response_model=List[schemas.Movie],
    responses={
        500: {"model": schemas.HTTPExceptionSchema, "description": "A fatal error"}
    },
)
def import_movies(db: Session = Depends(get_db)):
    try:
        files = list_files(config["imports"])
    except Exception as e:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"message": str(e)}
        )

    movies = []

    for file in files:
        name, _ = splitext(file)
        movie = crud.add_movie(db, file, name)
        if movie is not None:
            movies.append(movie)

    return movies


@app.post(
    "/actors",
    response_model=schemas.Actor,
    responses={
        409: {
            "model": schemas.HTTPExceptionSchema,
            "description": "Attempt to add duplicate actor",
        }
    },
)
def add_actor(data: schemas.MovieProperty, db: Session = Depends(get_db)):
    actor = crud.add_actor(db, data.name)
    if actor is None:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            detail={"message": f"Actor: {data.name} already in database"},
        )
    return actor


@app.get("/actors", response_model=List[schemas.Actor])
def get_actors(db: Session = Depends(get_db)):
    return crud.get_all_actors(db)


@app.get("/actors/{actor_id}")
def get_actor(actor_id: int, db: Session = Depends(get_db)):
    actor = crud.get_actor_by_id(actor_id, db)
    if actor is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail={"message": f"Actor with id {actor_id} was not found."},
        )
    return actor


@app.get("/actors/{name}/name")
def get_actor_by_name(name: str, db: Session = Depends(get_db)):
    actor = crud.get_actor_by_name(name, db)
    if actor is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail={"message": f"Actor with name {name} was not found."},
        )
    return actor


@app.get("/categories", response_model=List[schemas.Category])
def get_all_categories(db: Session = Depends(get_db)):
    return crud.get_all_categories(db)


@app.get("/categories/{category_id}", response_model=Optional[schemas.Category])
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = crud.get_category(db, category_id)
    if category is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail={"message": f"Category with id {category_id} was not found"},
        )
    return category


@app.get("/categories/{name}/name", response_model=Optional[schemas.Category])
def get_category_by_name(name: str, db: Session = Depends(get_db)):
    category = crud.get_category_by_name(db, name)
    if category is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail={"message": f"Category with name {name} was not found"},
        )
    return category


@app.post(
    "/categories",
    response_model=schemas.Category,
    responses={
        409: {"model": schemas.HTTPExceptionSchema, "description": "Duplicate Category"}
    },
)
def add_category(data: schemas.MovieProperty, db: Session = Depends(get_db)):
    category = crud.add_category(db, data.name)
    if category is None:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            detail={"message": f"Category {data.name} already in database"},
        )
    return category


@app.get("/studios", response_model=List[schemas.Studio])
def get_all_studios(db: Session = Depends(get_db)):
    return crud.get_all_studios(db)


@app.post(
    "/studios",
    response_model=schemas.Studio,
    responses={
        409: {"model": schemas.HTTPExceptionSchema, "description": "Duplicate Studio"}
    },
)
def add_studio(data: schemas.MovieProperty, db: Session = Depends(get_db)):
    studio = crud.add_studio(db, data.name)
    if studio is None:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            detail={"message": f"Studio {data.name} already in database"},
        )
    return studio


@app.get("/series", response_model=List[schemas.Series])
def get_all_series(db: Session = Depends(get_db)):
    return crud.get_all_series(db)


@app.post(
    "/series",
    response_model=schemas.Series,
    responses={
        409: {"model": schemas.HTTPExceptionSchema, "description": "Duplicate Series"}
    },
)
def add_series(data: schemas.MovieProperty, db: Session = Depends(get_db)):
    series = crud.add_series(db, data.name)
    if series is None:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            detail={"message": f"series {data.name} already in database"},
        )
    return series
