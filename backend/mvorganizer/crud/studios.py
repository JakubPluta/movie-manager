from sqlite3 import IntegrityError
from sqlalchemy.orm import Session
from typing import Optional, List

from ..exceptions import (
    DuplicateEntryException,
    InvalidIDException,
    IntegrityConstraintException,
)

from .. import schemas
from .. import models
from .. import utils
import logging
from sqlalchemy import func

logger = logging.getLogger(__name__)


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
    studio = models.Studio(name=name, sort_name=utils.generate_sort_name(name))

    try:
        db.add(studio)
        db.commit()
        db.refresh(studio)
    except Exception as e:
        db.rollback()
        raise DuplicateEntryException(f"Studio {name} already exists")

    return studio


def delete_studio(db: Session, studio_id: int) -> models.Studio:
    studio = get_studio_by_id(studio_id, db)
    if studio is None:
        raise InvalidIDException(f"Studio with id {studio_id} doesn't exists")
    try:
        db.delete(studio)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise IntegrityConstraintException(
            f"Studio {studio.name} exists at least one movie"
        )
    return studio


def update_studio(
    db: Session,
    id: int,
    name: str,
) -> models.Actor:
    studio = get_studio_by_id(id, db)

    if studio is None:
        raise InvalidIDException(f"Studio ID {id} does not exist")

    studio.name = name

    try:
        db.commit()
        db.refresh(studio)
    except IntegrityError:
        db.rollback()

        raise DuplicateEntryException(f"Studio {name} already exists")

    return studio
