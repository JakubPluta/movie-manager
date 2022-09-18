from sqlite3 import IntegrityError
from sqlalchemy.orm import Session
from typing import Optional, List

from .. import schemas
from .. import models
from .. import utils
import logging
from sqlalchemy import func

logger = logging.getLogger(__name__)


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


def get_actor_by_id(db: Session, id: int) -> models.Actor:
    return db.query(models.Actor).filter(models.Actor.id == id).first()


def get_actor_by_name(name: str, db: Session) -> models.Actor:
    return (
        db.query(models.Actor)
        .filter(func.lower(models.Actor.name) == func.lower(name))
        .first()
    )


def get_all_actors(db: Session) -> List[models.Actor]:
    return db.query(models.Actor).all()


def delete_actor(db: Session, actor: models.Actor) -> models.Actor:
    try:
        db.delete(actor)
        db.commit()
    except Exception as e:
        logger.error(f"Couldn't delete actor {actor}. {e} Doing rollback")
        db.rollback()
        return None
    return actor
