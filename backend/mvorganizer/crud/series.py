from sqlite3 import IntegrityError
from sqlalchemy.orm import Session
from typing import Optional, List

from ..exceptions import DuplicateEntryException, InvalidIDException

from .. import schemas
from .. import models
from .. import utils
import logging
from sqlalchemy import func

logger = logging.getLogger(__name__)


def get_series(db: Session, id: int) -> models.Series:
    return db.query(models.Series).filter(models.Series.id == id).first()


def get_series_by_name(db: Session, name: str) -> models.Series:
    return db.query(models.Series).filter(models.Series.name == name).first()


def get_all_series(db: Session) -> List[models.Series]:
    return db.query(models.Series).order_by(models.Series.name).all()


def add_series(db: Session, name: str) -> models.Series:
    series = models.Series(name=name, sort_name=utils.generate_sort_name(name))

    try:
        db.add(series)
        db.commit()
        db.refresh(series)
    except Exception as e:
        db.rollback()
        raise DuplicateEntryException(f"Series {name} already exists")

    return series


def delete_series(db: Session, series_id: int) -> models.Series:
    series = get_series(db, series_id)
    if series is None:
        raise InvalidIDException(f"Series with id {series_id} doesn't exists")

    try:
        db.delete(series)
        db.commit()
    except Exception as e:
        logger.error(f"Couldn't delete series {series}. {e} Doing rollback")
        db.rollback()
        raise e
    return series
