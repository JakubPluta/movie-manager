from sqlite3 import IntegrityError
from sqlalchemy.orm import Session
from typing import Optional, List

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


def delete_series(db: Session, series: models.Series) -> models.Series:
    try:
        db.delete(series)
        db.commit()
    except Exception as e:
        logger.error(f"Couldn't delete series {series}. {e} Doing rollback")
        db.rollback()
        return None
    return series
