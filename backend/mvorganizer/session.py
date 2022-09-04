import logging
from .base_db import SessionLocal


logger = logging.getLogger(__name__)

def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"sqlalchemy error: {str(e)}")
        db.rollback()

    finally:
        db.close()