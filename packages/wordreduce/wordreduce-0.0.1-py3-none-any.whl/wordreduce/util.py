import logging
import os

from logging import Formatter, getLogger, StreamHandler

SCRIPT_NAME = os.path.dirname(os.getcwd())

LOGGER = getLogger(SCRIPT_NAME)

formatter = Formatter(
    "%(asctime)s %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
handler = StreamHandler()
handler.setFormatter(formatter)

LOGGER.addHandler(handler)
LOGGER.setLevel(logging.INFO)