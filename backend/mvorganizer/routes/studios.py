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
from ..crud import studios_crud

router = APIRouter()




@router.get("", response_model=List[schemas.Studio])
def get_all_studios(db: Session = Depends(get_db)):
    return studios_crud.get_all_studios(db)


@router.get('/{studio_id}', response_model=schemas.Studio)
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
    studio = studios_crud.add_studio(db, data.name)
    if studio is None:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            detail={"message": f"Studio {data.name} already in database"},
        )
    return studio