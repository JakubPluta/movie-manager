from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException

from .. import schemas
from ..base_db import Session
from ..config import get_logger
from ..crud import studios_crud
from ..exceptions import (
    DuplicateEntryException,
    IntegrityConstraintException,
    InvalidIDException,
    PathException,
)
from ..session import get_db
from ..utils import rename_movie_file

logger = get_logger()

router = APIRouter()


@router.get("", response_model=List[schemas.Studio])
def get_all_studios(db: Session = Depends(get_db)):
    return studios_crud.get_all_studios(db)


@router.get("/{studio_id}", response_model=schemas.Studio)
def get_studio_by_id(*, db: Session = Depends(get_db), studio_id: int):
    return studios_crud.get_studio_by_id(studio_id, db)


@router.get("/{name}/name", response_model=schemas.Studio)
def get_studio_by_name(*, db: Session = Depends(get_db), name: str):
    return studios_crud.get_studio_by_name(name, db)


@router.post(
    "",
    response_model=schemas.Studio,
    responses={
        409: {
            "model": schemas.HTTPExceptionSchema,
            "description": "Duplicate Studio",
        }
    },
)
def add_studio(
    data: schemas.MoviePropertySchema, db: Session = Depends(get_db)
):
    try:
        studio = studios_crud.add_studio(db, data.name)
    except DuplicateEntryException as e:
        logger.warn(str(e))
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            detail={"message": str(e)},
        )
    return studio


@router.delete(
    "/{id}",
    responses={
        404: {
            "model": schemas.HTTPExceptionSchema,
            "description": "Invalid ID",
        },
        412: {
            "model": schemas.HTTPExceptionSchema,
            "description": "Integrity Constraint Failed",
        },
    },
)
def delete_studio(id: int, db: Session = Depends(get_db)):
    try:
        studios_crud.delete_studio(db, id)
    except InvalidIDException as e:
        logger.warn(str(e))
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail={"message": str(e)}
        )
    except IntegrityConstraintException as e:
        logger.warn(str(e))
        raise HTTPException(
            status.HTTP_412_PRECONDITION_FAILED, detail={"message": str(e)}
        )
    return {"message": f"Deleted studio ID {id}"}


@router.put(
    "/{id}",
    response_model=schemas.Studio,
    responses={
        404: {
            "model": schemas.HTTPExceptionSchema,
            "description": "Invalid ID",
        },
        409: {
            "model": schemas.HTTPExceptionSchema,
            "description": "Duplicate Studio",
        },
        500: {
            "model": schemas.HTTPExceptionSchema,
            "description": "Path Error",
        },
    },
)
def update_studio(
    id: int, data: schemas.MoviePropertySchema, db: Session = Depends(get_db)
):

    try:
        studio = studios_crud.get_studio_by_id(id, db)
        studio_name = studio.name

        studio = studios_crud.update_studio(db, id, data.name.strip())

        for movie in studio.movies:
            rename_movie_file(movie, studio_current=studio_name)

        db.commit()
    except DuplicateEntryException as e:
        logger.warn(str(e))
        raise HTTPException(
            status.HTTP_409_CONFLICT, detail={"message": str(e)}
        )
    except InvalidIDException as e:
        logger.warn(str(e))
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail={"message": str(e)}
        )
    except PathException as e:
        logger.warn(str(e))
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"message": str(e)}
        )
    return studio
