__version__ = "0.18.4"
__author__ = "GDSFactory"

import sys

from loguru import logger

logger.remove()
logger.add(
    sys.stdout,
    colorize=True,
    format="{time:HH:mm:ss} | <level>{level: <8}</level> | <level>{message}</level>",
)

from .app import app as app
from .info import *
from .schematic import *
from .viewer import *
from .watcher import *
from .yaml import *
