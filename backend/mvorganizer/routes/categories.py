from typing import List, Optional

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException

from .. import schemas
from ..base_db import Session
from ..config import get_logger
from ..crud import categories_crud
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


@router.get("", response_model=List[schemas.Category])
def get_all_categories(db: Session = Depends(get_db)):
    return categories_crud.get_all_categories(db)


@router.get("/{category_id}", response_model=Optional[schemas.Category])
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = categories_crud.get_category(db, category_id)
    if category is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail={
                "message": f"Category with id {category_id} was not found"
            },
        )
    return category


@router.get("/{name}/name", response_model=Optional[schemas.Category])
def get_category_by_name(name: str, db: Session = Depends(get_db)):
    category = categories_crud.get_category_by_name(db, name)
    if category is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail={"message": f"Category with name {name} was not found"},
        )
    return category


@router.post(
    "",
    response_model=schemas.Category,
    responses={
        409: {
            "model": schemas.HTTPExceptionSchema,
            "description": "Duplicate Category",
        }
    },
)
def add_category(
    data: schemas.MoviePropertySchema, db: Session = Depends(get_db)
):
    try:
        category = categories_crud.add_category(db, data.name)
    except DuplicateEntryException as e:
        logger.warn(str(e))
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            detail={"message": str(e)},
        )
    return category


@router.put(
    "/{id}",
    response_model=schemas.Category,
    responses={
        404: {
            "model": schemas.HTTPExceptionSchema,
            "description": "Invalid ID",
        },
        409: {
            "model": schemas.HTTPExceptionSchema,
            "description": "Duplicate Category",
        },
        500: {
            "model": schemas.HTTPExceptionSchema,
            "description": "Path Error",
        },
    },
)
def update_category(
    id: int, data: schemas.MoviePropertySchema, db: Session = Depends(get_db)
):
    try:
        category = categories_crud.get_category(db, id)
        category_name = category.name
        category = categories_crud.update_category(db, id, data.name.strip())

        for movie in category.movies:
            rename_movie_file(movie, category_current=category_name)
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
    return category


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
def delete_category(id: int, db: Session = Depends(get_db)):
    try:
        categories_crud.delete_category(db, id)
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

    return {"message": f"Deleted category ID {id}"}
