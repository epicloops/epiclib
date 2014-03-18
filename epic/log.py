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

def init(level='info'):

    level = LEVELS[level]

    logger = logging.getLogger()
    logger.setLevel(level)
    # create file handler
    fh = logging.FileHandler('epicpkg.log')
    fh.setLevel(level)
    # create console handler
    ch = logging.StreamHandler()
    ch.setLevel(level)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('[%(levelname)-8s] %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)
