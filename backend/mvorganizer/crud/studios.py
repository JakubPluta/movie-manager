from sqlite3 import IntegrityError
from sqlalchemy.orm import Session
from typing import Optional, List

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


def delete_studio(db: Session, studio: models.Studio) -> models.Studio:
    try:
        db.delete(studio)
        db.commit()
    except Exception as e:
        logger.error(f"Couldn't delete studio {studio}. {e} Doing rollback")
        db.rollback()
        return None
    return studio
