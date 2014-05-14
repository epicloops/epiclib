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

from epiclib.db.models import Base


log = logging.getLogger(__name__)


def engine(uri):
    return create_engine(uri)

def session(uri):
    return Session(bind=engine(uri))

@contextmanager
def session_scope(uri):
    '''Provide a transactional scope around a series of operations.'''
    sess = session(uri)
    try:
        yield sess
        sess.commit()
    except:
        sess.rollback()
        raise
    finally:
        sess.close()

def create(sqlalchemy_database_uri, *args, **kwargs):
    '''Create database schema.'''
    Base.metadata.create_all(engine(sqlalchemy_database_uri))
    log.info('Schema created.')

def truncate(sqlalchemy_database_uri, *args, **kwargs):
    '''Truncate all tables in database schema.'''
    for tbl in reversed(Base.metadata.sorted_tables):
        engine(sqlalchemy_database_uri).execute(tbl.delete())
        log.info('%s truncated.', tbl.name)

def drop(sqlalchemy_database_uri, *args, **kwargs):
    '''Drop database schema.'''
    Base.metadata.drop_all(engine(sqlalchemy_database_uri))
    log.info('Schema dropped.')
