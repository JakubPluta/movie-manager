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
from ..crud import categories_crud
from ..exceptions import (
    DuplicateEntryException,
    InvalidIDException,
    ListFilesException,
    PathException,
)

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
            detail={"message": f"Category with id {category_id} was not found"},
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
def add_category(data: schemas.MoviePropertySchema, db: Session = Depends(get_db)):
    try:
        category = categories_crud.add_category(db, data.name)
    except DuplicateEntryException as e:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            detail={"message": str(e)},
        )
    return category
