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
from ..crud import series_crud

router = APIRouter()





@router.get("/series", response_model=List[schemas.Series])
def get_all_series(db: Session = Depends(get_db)):
    return series_crud.get_all_series(db)


@router.post(
    "/series",
    response_model=schemas.Series,
    responses={
        409: {
            "model": schemas.HTTPExceptionSchema,
            "description": "Duplicate Series",
        }
    },
)
def add_series(data: schemas.MoviePropertySchema, db: Session = Depends(get_db)):
    series = series_crud.add_series(db, data.name)
    if series is None:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            detail={"message": f"series {data.name} already in database"},
        )
    return series


