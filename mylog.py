""" mylog v0.1
Simple module to handle logging configuration across multiple modules/libraries
"""
import logging


def get_logger(name=__name__):
    logger = logging.getLogger(name)
    h = logging.StreamHandler()
    h.setLevel(logging.INFO)
    f = logging.Formatter("%(levelname)s: %(name)s -  %(message)s")
    h.setFormatter(f)
    logger.addHandler(h)
    logger.setLevel(logging.INFO)
    return logger
