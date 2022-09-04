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
from typing import List
config = get_config()

app = FastAPI()

Base.metadata.create_all(bind=engine)




@app.get("/")
def home():
    return {"this is home"}


@app.post('/import_movies', response_model=List[schemas.Movie])
def import_movies(db: Session = Depends(get_db)):
    try:
        files = list_files(config['imports'])
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail={'message' : str(e)})
    
    movies = []

    for file in files:
        name, _ = splitext(file)
        movie = crud.add_movie(db, file, name)
        if movie is not None:
            movies.append(movie)

    return movies