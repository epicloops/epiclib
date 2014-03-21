# -*- coding: utf-8 -*-
'''
Manages the epic database backend.
'''
import os
import logging
import datetime
import time

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import epic.config as config
from epic.db.models import DeclarativeBase


log = logging.getLogger(__name__)


def make_engine():
    return create_engine(config.SQLALCHEMY_DATABASE_URI)

def session_maker():
    engine = make_engine()
    return sessionmaker(bind=engine)

def create(*args, **kwargs):
    '''Create database schema.'''
    engine = make_engine()
    DeclarativeBase.metadata.create_all(engine)
    log.info('Schema created.')

def truncate(*args, **kwargs):
    '''Truncate all tables in database schema.'''
    engine = make_engine()
    for tbl in reversed(DeclarativeBase.metadata.sorted_tables):
        engine.execute(tbl.delete())
        log.info('%s truncated.', tbl.name)

def drop(*args, **kwargs):
    '''Drop database schema.'''
    engine = make_engine()
    DeclarativeBase.metadata.drop_all(engine)
    log.info('Schema dropped.')
