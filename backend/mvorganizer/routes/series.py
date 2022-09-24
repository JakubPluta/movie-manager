from typing import List
from fastapi import APIRouter
from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from .. import schemas
from ..base_db import Session
from ..session import get_db
from ..crud import series_crud
from ..exceptions import DuplicateEntryException

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
        409: {"model": schemas.HTTPExceptionSchema, "description": "Duplicate Series"},
    },
)
def add_series(data: schemas.MoviePropertySchema, db: Session = Depends(get_db)):
    try:
        series = series_crud.add_series(db, data.name)
    except DuplicateEntryException as e:
        raise HTTPException(status.HTTP_409_CONFLICT, detail={"message": str(e)})

    return
