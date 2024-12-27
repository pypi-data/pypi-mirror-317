# function_caller/utils/logger.py

import logging
import sys
import os
from pathlib import Path
from colorlog import ColoredFormatter

def setup_logger(name: str, log_to_file: bool = False, log_to_console: bool = True):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Remove any existing handlers
    if logger.hasHandlers():
        logger.handlers.clear()

    formatter = ColoredFormatter(
        "%(log_color)s%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt='%Y-%m-%d %H:%M:%S',
        log_colors={
            'DEBUG':    'white',
            'INFO':     'green',
            'WARNING':  'yellow',
            'ERROR':    'red',
            'CRITICAL': 'bold_red',
        }
    )

    if log_to_console:
        # Console handler
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    if log_to_file:
        # Ensure the log directory exists
        log_dir = Path('logs')
        log_dir.mkdir(parents=True, exist_ok=True)
        # File handler
        fh = logging.FileHandler(log_dir / 'application.log')
        fh.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        fh.setFormatter(file_formatter)
        logger.addHandler(fh)

    return logger