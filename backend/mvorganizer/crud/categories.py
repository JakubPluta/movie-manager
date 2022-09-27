import logging
from sqlite3 import IntegrityError
from typing import List, Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from .. import models
from ..exceptions import (
    DuplicateEntryException,
    IntegrityConstraintException,
    InvalidIDException,
)

logger = logging.getLogger(__name__)


# Categories crud
def get_all_categories(db: Session) -> List[models.Category]:
    return db.query(models.Category).order_by(models.Category.name).all()


def get_category(db: Session, category_id: int) -> Optional[models.Category]:
    return (
        db.query(models.Category)
        .filter(models.Category.id == category_id)
        .first()
    )


def get_category_by_name(db: Session, name: str) -> Optional[models.Category]:
    return (
        db.query(models.Category)
        .filter(func.lower(models.Category.name) == func.lower(name))
        .first()
    )


def add_category(
    db: Session,
    name: str,
) -> models.Category:
    category = models.Category(name=name)

    try:
        db.add(category)
        db.commit()
        db.refresh(category)
    except IntegrityError:
        db.rollback()
        raise DuplicateEntryException(f"{category} already exists in database")

    return category


def delete_category(db: Session, category_id: int) -> models.Category:
    category = get_category(db, category_id)
    if category is None:
        raise InvalidIDException(
            f"Category with id {category_id} doesn't exists"
        )
    try:
        db.delete(category)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise IntegrityConstraintException(
            f"Category {category.name} exists at least one movie"
        )
    return category


def update_category(
    db: Session,
    id: int,
    name: str,
) -> models.Category:
    category = get_category(db, id)

    if category is None:
        raise InvalidIDException(f"Category ID {id} does not exist")

    category.name = name

    try:
        db.commit()
        db.refresh(category)
    except IntegrityError:
        db.rollback()

        raise DuplicateEntryException(f"Category {name} already exists")

    return category
