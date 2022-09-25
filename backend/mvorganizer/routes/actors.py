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
from ..exceptions import (
    DuplicateEntryException,
    InvalidIDException,
    IntegrityConstraintException,
)

router = APIRouter()


@router.post(
    "",
    response_model=schemas.Actor,
    responses={
        409: {
            "model": schemas.HTTPExceptionSchema,
            "description": "Attempt to add duplicate actor",
        }
    },
)
def add_actor(data: schemas.MoviePropertySchema, db: Session = Depends(get_db)):
    try:
        actor = actors_crud.add_actor(db, data.name)
    except DuplicateEntryException as e:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            detail={"message": str(e)},
        )
    return actor


@router.get("", response_model=List[schemas.Actor])
def get_actors(db: Session = Depends(get_db)):
    return actors_crud.get_all_actors(db)


@router.get("/{actor_id}")
def get_actor(actor_id: int, db: Session = Depends(get_db)):
    actor = actors_crud.get_actor_by_id(actor_id, db)
    if actor is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail={"message": f"Actor with id {actor_id} was not found."},
        )
    return actor


@router.get("/{name}/name")
def get_actor_by_name(name: str, db: Session = Depends(get_db)):
    actor = actors_crud.get_actor_by_name(name, db)
    if actor is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail={"message": f"Actor with name {name} was not found."},
        )
    return actor


@router.put(
    "/{id}",
    response_model=schemas.Actor,
    responses={
        404: {"model": schemas.HTTPExceptionSchema, "description": "Invalid ID"},
        409: {"model": schemas.HTTPExceptionSchema, "description": "Duplicate Actor"},
    },
)
def update_actor(
    id: int, data: schemas.MoviePropertySchema, db: Session = Depends(get_db)
):
    try:
        actor = actors_crud.update_actor(db, id, data.name.strip())
    except DuplicateEntryException as e:
        raise HTTPException(status.HTTP_409_CONFLICT, detail={"message": str(e)})
    except InvalidIDException as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail={"message": str(e)})

    return actor


@router.delete(
    "/{id}",
    responses={
        404: {"model": schemas.HTTPExceptionSchema, "description": "Invalid ID"},
        412: {
            "model": schemas.HTTPExceptionSchema,
            "description": "Integrity Constraint Failed",
        },
    },
)
def delete_actor(id: int, db: Session = Depends(get_db)):
    try:
        actors_crud.delete_actor(db, id)
    except InvalidIDException as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail={"message": str(e)})
    except IntegrityConstraintException as e:
        raise HTTPException(
            status.HTTP_412_PRECONDITION_FAILED, detail={"message": str(e)}
        )

    return {"message": f"Deleted actor ID {id}"}
