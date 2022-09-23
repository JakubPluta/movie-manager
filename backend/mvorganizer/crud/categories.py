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


# Categories crud
def get_all_categories(db: Session) -> List[models.Category]:
    return db.query(models.Category).order_by(models.Category.name).all()


def get_category(db: Session, category_id: int) -> Optional[models.Category]:
    return db.query(models.Category).filter(models.Category.id == category_id).first()


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
        raise InvalidIDException(f"Category with id {category_id} doesn't exists")
    try:
        db.delete(category)
        db.commit()
    except Exception as e:
        logger.error(f"Couldn't delete category {category}. {e} Doing rollback")
        db.rollback()
        raise e
    return category
