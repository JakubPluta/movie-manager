from sqlalchemy.orm import Session
from typing import Optional, List
from . import models
from . import utils 

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
    )

    if actor_ids is not None:
        movie.actors = actor_ids
    
    if category_ids is not None:
        movie.categories = category_ids

    db.add(movie)
    db.commit()
    db.refresh(movie)

    utils.migrate_file(movie)
    return movie