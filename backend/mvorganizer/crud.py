from sqlite3 import IntegrityError
from sqlalchemy.orm import Session
from typing import Optional, List
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
    return db.query(models.Actor).filter(
        models.Actor.id == id).first()

def get_actor_by_name(name: str, db: Session) -> models.Actor:
    return db.query(models.Actor).filter(
        func.lower(models.Actor.name) == func.lower(name)
        ).first()


def get_all_actors(db: Session) -> List[models.Actor]:
    return db.query(models.Actor).all()
