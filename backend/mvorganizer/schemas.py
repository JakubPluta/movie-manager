from typing import List, Optional

from pydantic import BaseModel


class BaseMovie(BaseModel):
    id: int
    filename: str

    class Config:
        orm_mode = True


class BaseMovieProperty(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class Actor(BaseMovieProperty):
    pass


class Category(BaseMovieProperty):
    pass


class Series(BaseMovieProperty):
    pass


class Studio(BaseMovieProperty):
    pass


class MovieFile(BaseMovie):
    pass


class MoviePropertySchema(BaseModel):
    name: str


class Movie(BaseMovie):
    name: Optional[str] = None
    actors: Optional[List[Actor]] = None
    categories: Optional[List[Category]] = None
    series: Optional[Series] = None
    series_number: Optional[int] = None
    studio: Optional[Studio] = None

    class Config:
        orm_mode = True


class MovieUpdateSchema(BaseModel):
    name: Optional[str] = None
    series_id: Optional[int] = None
    series_number: Optional[int] = None
    studio_id: Optional[int] = None


class HTTPExceptionMessage(BaseModel):
    message: str


class HTTPExceptionSchema(BaseModel):
    detail: HTTPExceptionMessage
