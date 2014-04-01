# -*- coding: utf-8 -*-
'''
Manages the epic database backend.
'''
import os
import logging
import datetime
import time
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import epic.config as config
from epic.db.models import Base


log = logging.getLogger(__name__)


def engine(echo=False):
    return create_engine(config.SQLALCHEMY_DATABASE_URI, echo=echo)

def session(echo=False):
    return Session(bind=engine(echo))

@contextmanager
def session_scope(echo=False):
    '''Provide a transactional scope around a series of operations.'''
    sess = session(echo)
    try:
        yield sess
        sess.commit()
    except:
        sess.rollback()
        raise
    finally:
        sess.close()

def create(*args, **kwargs):
    '''Create database schema.'''
    Base.metadata.create_all(engine())
    log.info('Schema created.')

def truncate(*args, **kwargs):
    '''Truncate all tables in database schema.'''
    for tbl in reversed(Base.metadata.sorted_tables):
        engine().execute(tbl.delete())
        log.info('%s truncated.', tbl.name)

def drop(*args, **kwargs):
    '''Drop database schema.'''
    Base.metadata.drop_all(engine())
    log.info('Schema dropped.')
