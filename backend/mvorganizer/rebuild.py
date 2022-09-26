import sys
from typing import Dict, List

from . import models
from . import utils
from .config import get_config
from .base_db import SessionLocal, engine
from .exceptions import ListFilesException
from .crud import actors_crud, movies_crud, series_crud, categories_crud, studios_crud


def run():
    config = get_config()

    # create the database tables and get a connection
    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # list the movie files
    try:
        movie_files = utils.list_files(config["movies"])
    except ListFilesException as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)

    # create lists of movie properties
    # seed them with the files in the link directories
    actors = []
    categories = []
    series = []
    studios = []

    for path in ("actors", "categories", "series", "studios"):
        files: List[str] = locals()[path]

        try:
            files.extend(utils.list_files(config[path]))
        except ListFilesException:
            pass

    movie_actors = {filename: [] for filename in movie_files}
    movie_categories = {filename: [] for filename in movie_files}
    movie_series = {filename: [] for filename in movie_files}
    movie_studios = {filename: [] for filename in movie_files}

    for path in ("actors", "categories", "series", "studios"):
        names: List[str] = locals()[path]

        for name in names:
            try:
                files = utils.list_files(f"{config[path]}/{name}")
            except ListFilesException:
                continue

            properties: Dict[str, List[str]] = locals()[f"movie_{path}"]

            for file in files:
                # if this test is false, it means there is a broken link
                # a link directory file is pointing at a non-existent movie file
                if file in properties:
                    properties[file].append(name)

    # get the remaining movie data from the movie files
    movie_name = {filename: None for filename in movie_files}
    movie_series_number = {filename: None for filename in movie_files}

    for file in movie_files:
        (
            name,
            studio_name,
            series_name,
            series_number,
            actor_names,
        ) = utils.parse_filename(file)

        if name is not None:
            movie_name[file] = name

        if actor_names is not None:
            file_actors = actor_names.split(", ")

            actors.extend(file_actors)
            movie_actors[file].extend(file_actors)

        if series_name is not None:
            series.append(series_name)
            movie_series[file].append(series_name)

        if series_number is not None:
            movie_series_number[file] = series_number

        if studio_name is not None:
            studios.append(studio_name)
            movie_studios[file].append(studio_name)

    # deduplicate and alphabetize the movie properties
    actors = sorted(set(actors))
    categories = sorted(set(categories))
    series = sorted(set(series))
    studios = sorted(set(studios))

    # create database entries for the movie properties
    # generate an association of names to DB entries
    actor_by_name = {
        actor.name: actor
        for actor in [actors_crud.add_actor(db, actor) for actor in actors]
    }

    category_by_name = {
        category.name: category
        for category in [
            categories_crud.add_category(db, category) for category in categories
        ]
    }

    series_by_name = {
        series.name: series
        for series in [series_crud.add_series(db, series) for series in series]
    }

    studio_by_name = {
        studio.name: studio
        for studio in [studios_crud.add_studio(db, studio) for studio in studios]
    }
    print(movie_files)

    # add the movies files to the database with their property associations
    for filename in movie_files:
        print(filename)
        name = movie_name[filename]
        series_number = movie_series_number[filename]
        series_id = None
        studio_id = None
        actors_list = None
        categories_list = None

        # if there is more than one series/studio after deduplication
        # it means something is odd with the link directories
        # no right answer here, so just pick one
        if len(movie_series[filename]) > 0:
            series_name = list(set(movie_series[filename]))[0]
            series_id = series_by_name[series_name].id

        if len(movie_studios[filename]) > 0:
            studio_name = list(set(movie_studios[filename]))[0]
            studio_id = studio_by_name[studio_name].id

        # deduplicate actors and categories
        # create a list of DB objects for the movie associations
        movie_actors_set = set(movie_actors[filename])
        actors_list = [actor_by_name[actor_name] for actor_name in movie_actors_set]

        movie_categories_set = set(movie_categories[filename])
        categories_list = [
            category_by_name[category_name] for category_name in movie_categories_set
        ]

        # add the movie to the database
        movies_crud.add_movie(
            db,
            filename,
            name,
            studio_id,
            series_id,
            series_number,
            actors_list,
            categories_list,
            True,
        )


if __name__ == "__main__":
    run()
