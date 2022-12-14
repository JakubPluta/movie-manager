import sys
from typing import Dict, List

from . import models, utils
from .base_db import SessionLocal, engine
from .config import init
from .crud import (
    actors_crud,
    categories_crud,
    movies_crud,
    series_crud,
    studios_crud,
)
from .exceptions import ListFilesException


def run():
    logger, config = init()

    # create the database tables and get a connection
    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    logger.info("Created sqlite table schemas")
    # list the movie files
    try:
        movie_files = utils.list_files(config["movies"])
    except ListFilesException as e:
        logger.critical(str(e))
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
            logger.info("Loaded %s from link directory %s", path, config[path])
        except ListFilesException:
            logger.warn(
                "Unable to load %s from link directory %s", path, config[path]
            )

    movie_actors = {filename: [] for filename in movie_files}
    movie_categories = {filename: [] for filename in movie_files}
    movie_series = {filename: [] for filename in movie_files}
    movie_studios = {filename: [] for filename in movie_files}

    for path in ("actors", "categories", "series", "studios"):
        names: List[str] = locals()[path]

        for name in names:
            try:
                full_path = f"{config[path]}/{name}"
                files = utils.list_files(full_path)
                logger.info("Loaded link files from %s", full_path)
            except ListFilesException:
                logger.error("Unable to read link files in %s", full_path)
                continue

            properties: Dict[str, List[str]] = locals()[f"movie_{path}"]

            for file in files:
                # if this test is false, it means there is a broken link
                # a link directory file is pointing at a non-existent movie file
                if file in properties:
                    properties[file].append(name)
                    logger.info(
                        "Associated movie %s with %s in %s", file, name, path
                    )

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
            logger.info("Parsed name %s from file %s", name, file)

        if actor_names is not None:
            file_actors = actor_names.split(", ")

            actors.extend(file_actors)
            movie_actors[file].extend(file_actors)
            logger.info("Parsed actors (%s) from file %s", actor_names, file)

        if series_name is not None:
            series.append(series_name)
            movie_series[file].append(series_name)
            logger.info("Parsed series %s from file %s", series_name, file)
        if series_number is not None:
            movie_series_number[file] = series_number
            logger.info(
                "Parsed series number %s from file %s", series_number, file
            )

        if studio_name is not None:
            studios.append(studio_name)
            movie_studios[file].append(studio_name)
            logger.info("Parsed studio %s from file %s", studio_name, file)

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
    logger.info("Imported actors into database")
    category_by_name = {
        category.name: category
        for category in [
            categories_crud.add_category(db, category)
            for category in categories
        ]
    }
    logger.info("Imported categories into database")
    series_by_name = {
        series.name: series
        for series in [series_crud.add_series(db, series) for series in series]
    }
    logger.info("Imported series into database")
    studio_by_name = {
        studio.name: studio
        for studio in [
            studios_crud.add_studio(db, studio) for studio in studios
        ]
    }
    logger.info("Imported studios into database")

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
        actors_list = [
            actor_by_name[actor_name] for actor_name in movie_actors_set
        ]

        movie_categories_set = set(movie_categories[filename])
        categories_list = [
            category_by_name[category_name]
            for category_name in movie_categories_set
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
        logger.info("Imported movie %s into database", filename)


if __name__ == "__main__":
    run()
