from os.path import splitext
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter, FastAPI
from fastapi import Depends, FastAPI, status
from fastapi.exceptions import HTTPException
from .. import schemas
from ..utils import list_files
from ..models import Base
from ..base_db import engine, Session
from ..session import get_db
from ..crud import actors_crud

router = APIRouter()




@router.post(
    "/actors",
    response_model=schemas.Actor,
    responses={
        409: {
            "model": schemas.HTTPExceptionSchema,
            "description": "Attempt to add duplicate actor",
        }
    },
)
def add_actor(data: schemas.MoviePropertySchema, db: Session = Depends(get_db)):
    actor = actors_crud.add_actor(db, data.name)
    if actor is None:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            detail={"message": f"Actor: {data.name} already in database"},
        )
    return actor


@router.get("/actors", response_model=List[schemas.Actor])
def get_actors(db: Session = Depends(get_db)):
    return actors_crud.get_all_actors(db)


@router.get("/actors/{actor_id}")
def get_actor(actor_id: int, db: Session = Depends(get_db)):
    actor = actors_crud.get_actor_by_id(actor_id, db)
    if actor is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail={"message": f"Actor with id {actor_id} was not found."},
        )
    return actor


@router.get("/actors/{name}/name")
def get_actor_by_name(name: str, db: Session = Depends(get_db)):
    actor = actors_crud.get_actor_by_name(name, db)
    if actor is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail={"message": f"Actor with name {name} was not found."},
        )
    return actor