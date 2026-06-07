"""
utils/logger.py
---------------
Centralised logger factory. Import get_logger() in any module
instead of calling logging.getLogger(__name__) directly, so
formatting stays consistent across the whole suite.
"""

import logging
import sys


def get_logger(name: str = "amazon_suite") -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(
            logging.Formatter(
                fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
                datefmt="%H:%M:%S",
            )
        )
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger
