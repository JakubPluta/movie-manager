import logging
import sys
from typing import Dict
import os
import yaml

DEFAULT_CONFIG_PATH = "./config.yaml"

logger = logging.getLogger(__name__)


def run_only_once(func):
    def helper(*args, **kwargs):
        if not helper.has_run:
            helper.has_run = True
            helper.data = func(*args, **kwargs)
        return helper.data

    helper.has_run = False
    return helper


@run_only_once
def get_config() -> Dict[str, str]:
    path = os.getenv("MOVIE_ORGANIZER_PATH", DEFAULT_CONFIG_PATH)
    data = None
    try:
        with open(path, "r") as f:
            data = yaml.safe_load(f)
    except:
        logger.info(f"Failed to read config file {path}", file=sys.stderr)
    return data
