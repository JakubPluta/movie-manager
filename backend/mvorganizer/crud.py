from sqlite3 import IntegrityError
from unicodedata import category
from sqlalchemy.orm import Session
from typing import Optional, List

from . import schemas
from . import models
from . import utils
import logging
from sqlalchemy import func

logger = logging.getLogger(__name__)


def add_movie(
    db: Session,
    filename: str,
    name: str,
    studio_id: Optional[int] = None,
    series_id: Optional[int] = None,
    series_number: Optional[int] = None,
    actor_ids: Optional[List[int]] = None,
    category_ids: Optional[List[int]] = None,
    processed: Optional[bool] = False,
) -> models.Movie:
    movie = models.Movie(
        filename=filename,
        name=name,
        studio_id=studio_id,
        series_id=series_id,
        series_number=series_number,
        processed=processed,
    )

    if actor_ids is not None:
        movie.actors = actor_ids

    if category_ids is not None:
        movie.categories = category_ids
    try:
        db.add(movie)
        db.commit()
        db.refresh(movie)
    except Exception as e:
        logger.error(f"SqlAlchemy exeption {str(e)}. Doing rollback")
        db.rollback()
        return None

    utils.migrate_file(movie)
    return movie


def update_movie(db: Session, id: int, data: schemas.MovieUpdateSchema) -> models.Movie:
    movie = get_movie_by_id(db, id)
    if movie is None:
        return None

    if all(
        [
            data.name == movie.name,
            data.series_id == movie.series_id,
            data.series_number == movie.series_number,
            data.studio_id == movie.studio_id,
        ]
    ):
        return movie

    for k, v in data.dict().items():
        setattr(movie, k, v)

    movie.processed = True if not movie.processed else movie.processed

    db.commit()
    db.refresh(movie)
    return movie


def get_all_movies(db: Session) -> List[models.Movie]:
    return (
        db.query(models.Movie)
        .outerjoin(models.Studio)
        .outerjoin(models.Series)
        .order_by(
            models.Movie.processed,
            models.Studio.name,
            models.Series.name,
            models.Movie.name,
        )
        .all()
    )


def get_movie_by_id(db: Session, movie_id: int) -> models.Movie:
    return db.query(models.Movie).filter(models.Movie.id == movie_id).first()


def get_movie_by_name(db: Session, name: str) -> models.Movie:
    return (
        db.query(models.Movie)
        .filter(func.lower(models.Movie.name) == func.lower(name))
        .first()
    )


def add_actor(db: Session, name: str) -> models.Actor:
    actor = models.Actor(name=name)

    try:
        db.add(actor)
        db.commit()
        db.refresh(actor)
    except Exception as e:
        logger.error(f"SqlAlchemy exeption {str(e)}. Doing rollback")
        db.rollback()
        return

    return actor


def get_actor_by_id(id: int, db: Session) -> models.Actor:
    return db.query(models.Actor).filter(models.Actor.id == id).first()


def get_actor_by_name(name: str, db: Session) -> models.Actor:
    return (
        db.query(models.Actor)
        .filter(func.lower(models.Actor.name) == func.lower(name))
        .first()
    )


def get_all_actors(db: Session) -> List[models.Actor]:
    return db.query(models.Actor).all()


def get_all_studios(db: Session) -> List[models.Studio]:
    return db.query(models.Studio).order_by(models.Studio.name).all()


def get_studio_by_name(name: str, db: Session) -> models.Actor:
    return (
        db.query(models.Studio)
        .filter(func.lower(models.Studio.name) == func.lower(name))
        .first()
    )


def get_studio_by_id(id: int, db: Session) -> models.Studio:
    return db.query(models.Studio).filter(models.Studio.id == id).first()


def add_studio(db: Session, name: str) -> models.Studio:
    studio = models.Studio(name=name)

    try:
        db.add(studio)
        db.commit()
        db.refresh(studio)
    except Exception as e:
        logger.error(f"SqlAlchemy exception {str(e)}. Doing rollback")
        db.rollback()
        return

    return studio


def get_all_series(db: Session) -> List[models.Series]:
    return db.query(models.Series).order_by(models.Series.name).all()


def add_series(db: Session, name: str) -> models.Series:
    series = models.Series(name=name)

    try:
        db.add(series)
        db.commit()
        db.refresh(series)
    except Exception as e:
        logger.error(f"SqlAlchemy exception {str(e)}. Doing rollback")
        db.rollback()
        return

    return series


# Categories crud
def get_all_categories(db: Session) -> List[models.Category]:
    return db.query(models.Category).order_by(models.Category.name).all()


def get_category(db: Session, category_id: int) -> Optional[models.Category]:
    return db.query(models.Category).filter(models.Category.id == category_id).first()


def get_category_by_name(db: Session, name: str) -> Optional[models.Category]:
    return (
        db.query(models.Category)
        .filter(func.lower(models.Category.name) == func.lower(name))
        .first()
    )


def add_category(db: Session, name: str) -> models.Category:
    category = models.Category(name=name)

    try:
        db.add(category)
        db.commit()
        db.refresh(category)
    except Exception as e:
        logger.error(f"SqlAlchemy exception {str(e)}. Doing rollback")
        db.rollback()
        return

    return category
