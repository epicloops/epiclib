# -*- coding: utf-8 -*-
'''
Filemanagers.
'''
import logging
import os
import shutil

from boto.s3.connection import S3Connection
from boto.s3.key import Key

from epic import config


log = logging.getLogger(__name__)


class S3FM(object):

    def __init__(self, crawl_id=None):
        self.conn = S3Connection(config.AWS_ACCESS_KEY_ID,
                                 config.AWS_SECRET_ACCESS_KEY,
                                 is_secure=False)
        self.bucket = self.conn.get_bucket(config.AWS_S3_BUCKET,
                                           validate=False)
        self._crawl_id = None
        self.crawl_id = crawl_id

    @property
    def crawl_id(self):
        if self._crawl_id is None:
            raise ValueError('crawl_id not set')
        return self._crawl_id

    @crawl_id.setter
    def crawl_id(self, value):
        self._crawl_id = value

    def abspath(self, path):
        if path.startswith(self.crawl_id):
            return path
        return '{0}/{1}'.format(self.crawl_id, path)

    def list(self, path=''):
        return self.bucket.list(self.abspath(path))

    def get_key(self, key):
        if isinstance(key, Key):
            return key
        abspath = self.abspath(key)
        return Key(self.bucket, abspath)

    def get(self, key, dest):
        k = self.get_key(key)
        if not os.path.exists(os.path.dirname(dest)):
            os.makedirs(os.path.dirname(dest))
        k.get_contents_to_filename(dest)
        log.info('Got s3 key: %s to %s', k.name, dest)
        return dest

    def _set(self, key, func, data, headers=None, policy='private'):
        k = self.get_key(key)
        getattr(k, func)(data, headers=headers, policy=policy)
        log.info('Set s3 key: %s', k.name)
        return k

    def set_from_string(self, key, string, headers=None, policy='private'):
        func = 'set_contents_from_string'
        return self._set(key, func, string, headers, policy)

    def set_from_file(self, key, fileobj, headers=None, policy='private'):
        func = 'set_contents_from_file'
        return self._set(key, func, fileobj, headers, policy)

    def set_from_filename(self, key, filename, headers=None, policy='private'):
        func = 'set_contents_from_filename'
        return self._set(key, func, filename, headers, policy)

    def generate_url(self, key, expires_in=300,  query_auth=True,
                     force_http=True):
        k = self.get_key(key)
        return k.generate_url(expires_in=expires_in, query_auth=query_auth,
                             force_http=force_http)


class LocalFM(object):

    def __init__(self):
        self.path = config.TMP_DIR

    def abspath(self, path):
        if path.startswith(self.path):
            return path
        return '{0}/{1}'.format(self.path, path)

    def mkdir(self, path):
        abspath = self.abspath(path)
        if not os.path.exists(abspath):
            os.makedirs(abspath)
            log.info('Created %s', abspath)
        return abspath

    def read(self, fname):
        return open(self.abspath(fname)).read()

    def write(self, fname, data):
        abspath = self.abspath(fname)
        with open(abspath, 'w') as f:
            f.write(data)
            log.info('Wrote to %s', abspath)
        return abspath

    def purge(self):
        if os.path.exists(self.path):
            shutil.rmtree(self.path)
            log.info('Removed %s', self.path)
