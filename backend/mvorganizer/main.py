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
from .routes import series_router, studios_router, movies_router, categories_router, actors_router

config = get_config()

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https?://(?:127\.0\.0\.1|localhost):300[0-9]",
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(movies_router, prefix='/movies', tags=['movies'])
app.include_router(actors_router, prefix='/actors', tags=['actors'])
app.include_router(categories_router, prefix='/categories', tags=['categories'])
app.include_router(studios_router, prefix='/studios', tags=['studios'])
app.include_router(series_router, prefix='/series', tags=['series'])

@app.get("/")
def hello():
    return "Hello from FastAPI"

