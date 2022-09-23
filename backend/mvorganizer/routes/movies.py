from os.path import splitext
from typing import List, Optional, Union
from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter, FastAPI
from fastapi import Depends, FastAPI, status
from fastapi.exceptions import HTTPException
from .. import schemas
from ..utils import list_files
from ..models import Base
from ..base_db import engine, Session
from ..session import get_db
from ..crud import movies_crud
from ..config import get_config
from ..exceptions import (
    DuplicateEntryException,
    InvalidIDException,
    ListFilesException,
    PathException,
)

config = get_config()

router = APIRouter()


@router.get("", response_model=List[schemas.MovieFile])
def get_all_movies(db: Session = Depends(get_db)):
    return movies_crud.get_all_movies(db)


@router.get(
    "/{movie_id}",
    response_model=schemas.Movie,
    responses={
        404: {
            "model": schemas.HTTPExceptionSchema,
            "description": "Invalid ID",
        }
    },
)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = movies_crud.get_movie_by_id(db, movie_id)
    if movie is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail={"message": f"Movie with id {movie_id} does not exist"},
        )
    return movie


@router.post(
    "",
    response_model=List[schemas.Movie],
    responses={
        500: {
            "model": schemas.HTTPExceptionSchema,
            "description": "A fatal error",
        }
    },
)
def import_movies(db: Session = Depends(get_db)):
    try:
        files = list_files(config["imports"])
    except Exception as e:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"message": str(e)}
        )

    movies = []

    for file in files:
        name, _ = splitext(file)
        movie = movies_crud.add_movie(db, file, name)
        if movie is not None:
            movies.append(movie)

    return movies


@router.put(
    "/{movie_id}",
    response_model=schemas.Movie,
    responses={
        404: {
            "model": schemas.HTTPExceptionSchema,
            "description": "Invalid ID",
        }
    },
)
def update_movie(
    movie_id: int, data: schemas.MovieUpdateSchema, db: Session = Depends(get_db)
):
    movie = movies_crud.update_movie(db, movie_id, data)
    if movie is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail={"message": f"Movie with id {movie_id} does not exist"},
        )

    return movie


@router.delete("/{movie_id}")
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = movies_crud.get_movie_by_id(db, movie_id)
    if movie is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail={"message": f"movie with id {movie_id} doest not exist in database"},
        )

    deleted_movie = movies_crud.delete_movie(db, movie)
    if deleted_movie is None:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail={
                "message": f"Something went wrong. Couldn't delete movie {movie.name} with id {movie_id}"
            },
        )
    return {"message": f"movie with {movie_id} deleted"}


@router.post(
    "/movie_category",
    response_model=schemas.Movie,
    responses={
        404: {"model": schemas.HTTPExceptionSchema, "description": "Invalid ID"},
        409: {
            "model": schemas.HTTPExceptionSchema,
            "description": "Duplicate Category",
        },
        500: {"model": schemas.HTTPExceptionSchema, "description": "Path Error"},
    },
)
def add_movie_category(movie_id: int, category_id: int, db: Session = Depends(get_db)):
    try:
        movie = movies_crud.add_movie_category(db, movie_id, category_id)
    except DuplicateEntryException as e:
        raise HTTPException(status.HTTP_409_CONFLICT, detail={"message": str(e)})
    except InvalidIDException as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail={"message": str(e)})
    except PathException as e:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"message": str(e)}
        )

    return movie


@router.delete(
    "/movie_category",
    response_model=schemas.Movie,
    responses={
        404: {"model": schemas.HTTPExceptionSchema, "description": "Invalid ID"},
        500: {"model": schemas.HTTPExceptionSchema, "description": "Path Error"},
    },
)
def delete_movie_category(
    movie_id: int, category_id: int, db: Session = Depends(get_db)
):
    try:
        movie = movies_crud.delete_movie_category(db, movie_id, category_id)
    except InvalidIDException as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail={"message": str(e)})
    except PathException as e:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"message": str(e)}
        )

    return movie


@router.post(
    "/movie_actor/",
    response_model=schemas.Movie,
    responses={
        404: {"model": schemas.HTTPExceptionSchema, "description": "Invalid ID"},
        409: {"model": schemas.HTTPExceptionSchema, "description": "Duplicate Actor"},
        500: {"model": schemas.HTTPExceptionSchema, "description": "Path Error"},
    },
)
def add_movie_actor(movie_id: int, actor_id: int, db: Session = Depends(get_db)):
    try:
        movie = movies_crud.add_movie_actor(db, movie_id, actor_id)
    except DuplicateEntryException as e:
        raise HTTPException(status.HTTP_409_CONFLICT, detail={"message": str(e)})
    except InvalidIDException as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail={"message": str(e)})
    except PathException as e:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"message": str(e)}
        )

    return movie


@router.delete(
    "/movie_actor/",
    response_model=schemas.Movie,
    responses={
        404: {"model": schemas.HTTPExceptionSchema, "description": "Invalid ID"},
        500: {"model": schemas.HTTPExceptionSchema, "description": "Path Error"},
    },
)
def delete_movie_actor(
    movie_id: Union[int, str], actor_id: int, db: Session = Depends(get_db)
):
    try:
        movie = movies_crud.delete_movie_actor(db, movie_id, actor_id)
    except InvalidIDException as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail={"message": str(e)})
    except PathException as e:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"message": str(e)}
        )

    return movie
