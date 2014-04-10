# -*- coding: utf-8 -*-
'''
Basic logging setup.
'''
import logging


LEVELS = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL
}

LEVEL_KEYS = sorted(LEVELS.iterkeys(), key=lambda k: LEVELS[k])


def init(level, logfile):

    level_idx = LEVEL_KEYS.index(level)
    level = LEVELS[level]
    down_idx = level_idx-1 if level_idx-1 >= 0 else level_idx
    down_level = LEVELS[LEVEL_KEYS[down_idx]]
    up_idx = level_idx+1 if level_idx+1 <= len(LEVEL_KEYS)-1 else level_idx
    up_level = LEVELS[LEVEL_KEYS[up_idx]]


    # configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    ch = logging.StreamHandler()
    fh = logging.FileHandler(logfile)
    ch.setLevel(level)
    fh.setLevel(level)

    formatter = logging.Formatter('[%(asctime)s][%(levelname)-8s][%(name)s] '
                                  '%(message)s')
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    root_logger.addHandler(ch)
    root_logger.addHandler(fh)


    # configure sqlalchemy loggers
    logging.getLogger('sqlalchemy.engine').setLevel(up_level)
    # logging.getLogger('sqlalchemy.dialects').setLevel(level)
    # logging.getLogger('sqlalchemy.pool').setLevel(level)
    logging.getLogger('sqlalchemy.orm').setLevel(up_level)


    # configure boto logging
    logging.getLogger('boto').setLevel(level)
