# -*- coding: utf-8 -*-
'''
s3 filestores.
'''
import logging
import os

from boto.s3.connection import S3Connection
from boto.s3.key import Key

from epic import config


log = logging.getLogger(__name__)


class RootStore(object):
    '''Base class for s3 filestore relative to bucket root.'''

    def __init__(self):
        self.conn = S3Connection(config.AWS_ACCESS_KEY_ID,
                                 config.AWS_SECRET_ACCESS_KEY,
                                 is_secure=False)
        self.bucket = self.conn.get_bucket(config.AWS_S3_BUCKET,
                                           validate=False)

    def list(self, path=''):
        return self.bucket.list(path)

    def get_key(self, key):
        if isinstance(key, Key):
            return key
        return Key(self.bucket, key)

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


class SubStore(RootStore):
    '''Base class for s3 filestore relative to a path from bucket root.'''

    def __init__(self, prefix):
        super(SubStore, self).__init__()
        self.prefix = prefix

    def _prepend_prefix(self, path):
        return '{0}/{1}'.format(self.prefix, path)

    def list(self, path=''):
        full_path = self._prepend_prefix(path)
        return super(SubStore, self).list(full_path)

    def get_key(self, key):
        if isinstance(key, Key):
            if not key.name.startswith(self.prefix):
                raise
            return key

        full_key = self._prepend_prefix(key)
        return Key(self.bucket, full_key)


class BotStore(SubStore):

    def __init__(self, crawl_start, spider):
        prefix = 'bot/{0}/{1}'.format(crawl_start, spider)
        super(BotStore, self).__init__(prefix)


class SamplerStore(SubStore):

    def __init__(self, crawl_start, spider, sampler_start):
        prefix = 'sampler/{0}/{1}/{2}'.format(crawl_start, spider,
                                              sampler_start)
        super(SamplerStore, self).__init__(prefix)


class PkgStore(SubStore):

    def __init__(self):
        prefix = 'pkg'
        super(PkgStore, self).__init__(prefix)
