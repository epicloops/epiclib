# -*- coding: utf-8 -*-
'''
Manange interaction with s3.
'''
import logging
import os

from boto.s3.connection import S3Connection
from boto.s3.key import Key

from epic import config


log = logging.getLogger(__name__)


def get_conn():
    # disable ssl (is_secure=False) because of this python bug:
    # http://bugs.python.org/issue5103
    return S3Connection(config.AWS_ACCESS_KEY_ID,
                        config.AWS_SECRET_ACCESS_KEY,
                        is_secure=False)

def get_bucket():
    conn = get_conn()
    return conn.get_bucket(config.AWS_S3_BUCKET, validate=False)

def list(path):
    bucket = get_bucket()
    return bucket.list(path)

def get_key(key_name):
    bucket = get_bucket()
    return Key(bucket, key_name)

def get(key_name, dest):
    k = get_key(key_name)
    if not os.path.exists(os.path.dirname(dest)):
        os.makedirs(os.path.dirname(dest))
    k.get_contents_to_filename(dest)
    log.info('Got s3 key: %s to %s', k.name, dest)
    return dest

def _set(key_name, func, data, headers=None, policy='private'):
    k = get_key(key_name)
    getattr(k, func)(data, headers=headers, policy=policy)
    log.info('Set s3 key: %s', k.name)
    return k

def set_from_string(key_name, string, headers=None, policy='private'):
    func = 'set_contents_from_string'
    return _set(key_name, func, string, headers, policy)

def set_from_file(key_name, fileobj, headers=None, policy='private'):
    func = 'set_contents_from_file'
    return _set(key_name, func, fileobj, headers, policy)

def set_from_filename(key_name, filename, headers=None, policy='private'):
    func = 'set_contents_from_filename'
    return _set(key_name, func, filename, headers, policy)

def generate_url(key_name, expires_in=300,  query_auth=True, force_http=True):
    k = get_key(key_name)
    return k.generate_url(expires_in=expires_in, query_auth=query_auth,
                         force_http=force_http)
