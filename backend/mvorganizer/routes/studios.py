from typing import List
from fastapi import APIRouter
from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from .. import schemas
from ..base_db import Session
from ..session import get_db
from ..crud import studios_crud
from ..exceptions import DuplicateEntryException

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
def add_studio(data: schemas.MoviePropertySchema, db: Session = Depends(get_db)):
    try:
        studio = studios_crud.add_studio(db, data.name)
    except DuplicateEntryException as e:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            detail={"message": str(e)},
        )
    return studio
