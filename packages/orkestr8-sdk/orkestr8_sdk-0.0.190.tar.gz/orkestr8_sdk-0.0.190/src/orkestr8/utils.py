import logging
import os
from pathlib import Path

from orkestr8.settings import LOG_OUTPUT_FILE_LOCATION


def create_file_if_not_exists(file_path: Path) -> None:
    """Wrapper to ensure `file_path` exists, even if empty"""
    if Path(file_path).exists():
        return
    os.makedirs(str(file_path.parent), exist_ok=True)
    with open(str(file_path), "w"):
        pass


def setup_logging():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("app")
    logger.setLevel(logging.INFO)

    format = "[%(asctime)s]: %(message)s"
    formatter = logging.Formatter(fmt=format, datefmt="%Y-%m-%d %H:%M:%S")
    handler = logging.FileHandler(LOG_OUTPUT_FILE_LOCATION)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
