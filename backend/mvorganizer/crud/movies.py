import logging
from sqlite3 import IntegrityError
from typing import List, Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from .. import models, schemas, utils
from ..exceptions import DuplicateEntryException, InvalidIDException
from .actors import get_actor_by_id
from .categories import get_category
from .series import get_series
from .studios import get_studio_by_id

logger = logging.getLogger(__name__)


def get_all_movies(db: Session) -> List[models.Movie]:
    return (
        db.query(models.Movie)
        .outerjoin(models.Studio)
        .outerjoin(models.Series)
        .order_by(
            models.Movie.processed,
            models.Studio.sort_name,
            models.Series.sort_name,
            models.Movie.sort_name,
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
        sort_name=utils.generate_sort_name(name),
    )

    if actor_ids is not None:
        movie.actors = actor_ids

    if category_ids is not None:
        movie.categories = category_ids
    try:
        db.add(movie)
        db.commit()
        db.refresh(movie)
    except IntegrityError as e:
        db.rollback()
        raise DuplicateEntryException(f"{movie} already exists in database")

    return movie


def update_movie(
    db: Session, id: int, data: schemas.MovieUpdateSchema
) -> models.Movie:
    movie = get_movie_by_id(db, id)
    if movie is None:
        raise InvalidIDException(f"Movie ID {id} does not exist")
    if all(
        [
            data.name == movie.name,
            data.series_id == movie.series_id,
            data.series_number == movie.series_number,
            data.studio_id == movie.studio_id,
        ]
    ):
        return movie

    if movie.name != data.name:
        movie.sort_name = utils.generate_sort_name(data.name)

    if movie.series_id != data.series_id:
        series_current = (
            get_series(db, movie.series_id).name
            if movie.series_id is not None
            else None
        )
        series_new = (
            get_series(db, data.series_id).name
            if data.series_id is not None
            else None
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
            get_studio_by_id(movie.studio_id, db).name
            if movie.studio_id is not None
            else None
        )
        studio_new = (
            get_studio_by_id(data.studio_id, db).name
            if data.studio_id is not None
            else None
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


def delete_movie(
    db: Session,
    id: int,
) -> None:
    movie = get_movie_by_id(db, id)

    if movie is None:
        raise InvalidIDException(f"Movie ID {id} does not exist")

    utils.remove_movie(movie)

    db.delete(movie)
    db.commit()


def add_movie_actor(db: Session, movie_id: int, actor_id: int) -> models.Movie:
    movie = get_movie_by_id(db, movie_id)
    if movie is None:
        raise InvalidIDException(f"Movie ID {movie_id} does not exist")

    actor = get_actor_by_id(db, actor_id)

    if actor is None:
        raise InvalidIDException(f"Actor ID {actor_id} does not exist")

    for movie_actor in movie.actors:
        if actor_id == movie_actor.id:
            raise DuplicateEntryException(
                f"Actor ID {actor_id} is already on Movie ID {movie_id}"
            )
    movie.actors.append(actor)
    db.commit()

    utils.rename_movie_file(movie)
    try:
        utils.update_actor_link(movie.filename, actor.name, True)
    except Exception as e:
        logger.error(str(e))
    db.commit()
    db.refresh(movie)

    return movie


def delete_movie_actor(
    db: Session, movie_id: int, actor_id: int
) -> models.Movie:
    movie = get_movie_by_id(db, movie_id)

    if movie is None:
        raise InvalidIDException(f"Movie ID {movie_id} does not exist")

    actor = get_actor_by_id(db, actor_id)

    if actor is None:
        raise InvalidIDException(f"Actor ID {actor_id} does not exist")

    if actor in movie.actors:
        movie.actors.remove(actor)
        try:
            utils.update_actor_link(movie.filename, actor.name, False)
        except Exception as e:
            logger.error(str(e))
        db.commit()
        db.refresh(movie)

    return movie


def add_movie_category(
    db: Session, movie_id: int, category_id: int
) -> models.Movie:
    movie = get_movie_by_id(db, movie_id)
    category = get_category(db, category_id)
    if movie is None:
        raise InvalidIDException(f"Movie ID {movie_id} does not exist")

    if category is None:
        raise InvalidIDException(f"category ID {category_id} does not exist")

    movie_category: models.Category
    for movie_category in movie.categories:
        if category_id == movie_category.id:
            raise DuplicateEntryException(
                f"Category ID {category_id} is already on Movie ID {movie_id}"
            )

    movie.categories.append(category)
    db.commit()

    try:
        utils.update_category_link(movie.filename, category.name, True)
    except Exception as e:
        logger.error(f"update category link error: {str(e)}")
    db.commit()
    db.refresh(movie)

    return movie


def delete_movie_category(
    db: Session, movie_id: int, category_id: int
) -> models.Movie:
    movie = get_movie_by_id(db, movie_id)

    if movie is None:
        raise InvalidIDException(f"Movie ID {movie_id} does not exist")

    category = get_category(db, category_id)

    if category is None:
        raise InvalidIDException(f"Category ID {category_id} does not exist")

    if category in movie.categories:
        movie.categories.remove(category)

        try:
            utils.update_category_link(movie.filename, category.name, False)
        except Exception as e:
            logger.error(f"update category link error: {str(e)}")

    db.commit()
    db.refresh(movie)

    return movie
