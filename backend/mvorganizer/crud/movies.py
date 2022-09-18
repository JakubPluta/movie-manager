from sqlite3 import IntegrityError
from sqlalchemy.orm import Session
from typing import Optional, List

from .. import schemas
from .. import models
from .. import utils
import logging
from sqlalchemy import func

logger = logging.getLogger(__name__)


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

    if movie.series_id != data.series_id:
        series_current = (
            get_series(db, movie.series_id).name
            if movie.series_id is not None
            else None
        )
        series_new = (
            get_series(db, data.series_id).name if data.series_id is not None else None
        )

        if data.series_id is None:
            utils.update_series_link(movie.filename, series_current, False)
        elif movie.series_id is None:
            # add series
            utils.update_series_link(movie.filename, series_new, True)
        else:
            # change series
            utils.update_series_link(movie.filename, series_current, False)
            utils.update_series_link(movie.filename, series_new, True)

    if movie.studio_id != data.studio_id:
        studio_current = (
            get_studio(db, movie.studio_id).name
            if movie.studio_id is not None
            else None
        )
        studio_new = (
            get_studio(db, data.studio_id).name if data.studio_id is not None else None
        )

        if data.studio_id is None:
            # remove studio
            utils.update_studio_link(movie.filename, studio_current, False)
        elif movie.studio_id is None:
            # add studio
            utils.update_studio_link(movie.filename, studio_new, True)
        else:
            # change studio
            utils.update_studio_link(movie.filename, studio_current, False)
            utils.update_studio_link(movie.filename, studio_new, True)
    for k, v in data.dict().items():
        setattr(movie, k, v)
    movie.processed = True if not movie.processed else movie.processed

    utils.rename_movie_file(movie)
    db.commit()
    db.refresh(movie)
    return movie


def delete_movie(db: Session, movie: models.Movie) -> models.Movie:
    try:
        db.delete(movie)
        db.commit()
    except Exception as e:
        logger.error(f"Couldn't delete movie {movie}. {e} Doing rollback")
        db.rollback()
        return None
    return movie


def add_movie_actor(db: Session, movie_id: int, actor_id: int) -> models.Movie:
    movie = get_movie_by_id(db, movie_id)
    actor = get_actor_by_id(db, actor_id)

    if movie is None or actor is None:
        return None

    movie.actors.append(actor)
    utils.rename_movie_file(movie)
    try:
        utils.update_actor_link(movie.filename, actor.name, True)
    except Exception as e:
        logger.error(str(e))
    db.commit()
    db.refresh(movie)

    return movie


def delete_movie_actor(db: Session, movie_id: int, actor_id: int) -> models.Movie:
    movie = get_movie_by_id(db, movie_id)
    actor = get_actor_by_id(db, actor_id)

    if movie is None or actor is None:
        return None

    if actor in movie.actors:
        movie.actors.remove(actor)
        try:
            utils.update_actor_link(movie.filename, actor.name, False)
        except Exception as e:
            logger.error(str(e))
        db.commit()
        db.refresh(movie)

    return movie


def add_movie_category(db: Session, movie_id: int, category_id: int) -> models.Movie:
    movie = get_movie_by_id(db, movie_id)
    category = get_category(db, category_id)
    if movie is None or category is None:
        return None

    movie.categories.append(category)
    try:
        utils.update_category_link(movie.filename, category.name, True)
    except Exception as e:
        logger.error(f"update category link error: {str(e)}")
    db.commit()
    db.refresh(movie)

    return movie


def delete_movie_category(db: Session, movie_id: int, category_id: int) -> models.Movie:
    movie = get_movie_by_id(db, movie_id)
    category = get_category(db, category_id)

    if movie is None or category is None:
        return None
    if category in movie.categories:
        movie.categories.remove(category)

        try:
            utils.update_category_link(movie.filename, category.name, False)
        except Exception as e:
            logger.error(f"update category link error: {str(e)}")

    db.commit()
    db.refresh(movie)

    return movie
