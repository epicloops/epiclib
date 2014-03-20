'''
Manages the epic database backend.
'''
import os
import logging
import datetime
import time

import boto.rds

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import epic.config as config
from epic.db.models import DeclarativeBase


log = logging.getLogger(__name__)


def _rds_connection():
    return boto.rds.connect_to_region('us-east-1',
                        aws_access_key_id=config.AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY)

def up(snapshot, *args, **kwargs):
    '''Bring up RDS instance from snapshot.'''
    conn = _rds_connection()
    db = conn.restore_dbinstance_from_dbsnapshot(snapshot, 'epic',
                    'db.t1.micro', port=5432, availability_zone='us-east-1d',
                    multi_az=False)
    log.info('Waiting for instance to become available.')
    while True:
        db = conn.get_all_dbinstances(instance_id='epic')[0]
        log.info('Status: %s', db.status)
        if db.status == 'available':
            break
        time.sleep(30)
    log.info('Endpoint: %s', db.endpoint)

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

def destroy(skip_snapshot, *args, **kwargs):
    '''Destroy RDS instance.'''
    conn = _rds_connection()
    db = conn.get_all_dbinstances(instance_id='epic')[0]

    snapshot=None
    if not skip_snapshot:
        snapshot = 'epic-{:%Y-%m-%dT%H-%M-%S}'.format(datetime.datetime.now())
        log.info('Snapshot: %s', snapshot)

    stopped = db.stop(skip_final_snapshot=skip_snapshot, final_snapshot_id=snapshot)
    log.info('Stopped: %s', stopped)
