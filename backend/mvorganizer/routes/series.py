from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException

from .. import schemas
from ..base_db import Session
from ..config import get_logger
from ..crud import series_crud
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


@router.get("", response_model=List[schemas.Series])
def get_all_series(db: Session = Depends(get_db)):
    return series_crud.get_all_series(db)


@router.get("/{series_id}", response_model=schemas.Series)
def get_all_series(*, db: Session = Depends(get_db), series_id: int):
    return series_crud.get_series(db, id)


@router.post(
    "",
    response_model=schemas.Series,
    responses={
        409: {
            "model": schemas.HTTPExceptionSchema,
            "description": "Duplicate Series",
        },
    },
)
def add_series(
    data: schemas.MoviePropertySchema, db: Session = Depends(get_db)
):
    try:
        series = series_crud.add_series(db, data.name)
    except DuplicateEntryException as e:
        logger.warn(str(e))
        raise HTTPException(
            status.HTTP_409_CONFLICT, detail={"message": str(e)}
        )

    return series


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
def delete_series(id: int, db: Session = Depends(get_db)):
    try:
        series_crud.delete_series(db, id)
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
    return {"message": f"Deleted series ID {id}"}


@router.put(
    "/{id}",
    response_model=schemas.Series,
    responses={
        404: {
            "model": schemas.HTTPExceptionSchema,
            "description": "Invalid ID",
        },
        409: {
            "model": schemas.HTTPExceptionSchema,
            "description": "Duplicate Series",
        },
        500: {
            "model": schemas.HTTPExceptionSchema,
            "description": "Path Error",
        },
    },
)
def update_series(
    id: int, data: schemas.MoviePropertySchema, db: Session = Depends(get_db)
):
    try:
        series = series_crud.get_series(db, id)
        series_name = series.name
        series = series_crud.update_series(db, id, data.name.strip())

        for movie in series.movies:
            rename_movie_file(movie, series_current=series_name)
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
    return series
