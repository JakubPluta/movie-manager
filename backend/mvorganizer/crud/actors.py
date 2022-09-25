from sqlite3 import IntegrityError
from sqlalchemy.orm import Session
from typing import List

from .. import models
from ..exceptions import (
    DuplicateEntryException,
    InvalidIDException,
    IntegrityConstraintException,
)
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
        db.rollback()
        raise DuplicateEntryException(f"Actor {name} already exists")

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


def delete_actor(db: Session, actor_id: int) -> models.Actor:
    actor = get_actor_by_id(db, actor_id)
    if actor is None:
        raise InvalidIDException(f"Actor ID {id} does not exist")

    try:
        db.delete(actor)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise IntegrityConstraintException(
            f"Actor {actor.name} exists at least one movie"
        )
    return actor


def update_actor(
    db: Session,
    id: int,
    name: str,
) -> models.Actor:
    actor = get_actor_by_id(db, id)

    if actor is None:
        raise InvalidIDException(f"Actor ID {id} does not exist")

    actor.name = name

    try:
        db.commit()
        db.refresh(actor)
    except IntegrityError:
        db.rollback()

        raise DuplicateEntryException(f"Actor {name} already exists")

    return actor
