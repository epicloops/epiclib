# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from boto.s3.connection import S3Connection

from twisted.internet import threads

from scrapy import signals


class S3FileStore(object):

    def __init__(self, crawler):
        self.stats = crawler.stats
        self.settings = crawler.settings
        self.aws_access_key_id = self.settings.get('AWS_ACCESS_KEY_ID')
        self.aws_secret_access_key = self.settings.get('AWS_SECRET_ACCESS_KEY')
        self.bucket = self.settings.get('AWS_S3_BUCKET')
        self.prefix = {}

    @classmethod
    def from_crawler(cls, crawler):
        ext = cls(crawler)
        crawler.signals.connect(ext.spider_opened, signals.spider_opened)
        return ext

    def spider_opened(self, spider):
        st = '{:%Y-%m-%dT%H-%M-%S}'.format(self.stats.get_value('start_time'))
        self.prefix[spider] = '/'.join(['bot', st, spider.name])

    def _get_bucket(self):
        # disable ssl (is_secure=False) because of this python bug:
        # http://bugs.python.org/issue5103
        # TODO: use deferred?
        c = S3Connection(self.aws_access_key_id, self.aws_secret_access_key,
                         is_secure=False)
        return c.get_bucket(self.bucket, validate=False)

    def _get_new_key(self, spider, path, meta):
        # TODO: use deferred?
        b = self._get_bucket()
        key_name = '/'.join([self.prefix[spider], path])
        k = b.new_key(key_name)
        if meta:
            for metakey, metavalue in meta.iteritems():
                k.set_metadata(metakey, str(metavalue))
        return k

    def _write(self, key, obj, headers, policy):
        try:
            obj.seek(0)
            key.set_contents_from_file(obj, headers=headers,
                                       policy=policy)
        except AttributeError:
            key.set_contents_from_string(obj, headers=headers,
                                         policy=policy)

    def write(self, spider, path, obj, meta=None, headers=None):
        k = self._get_new_key(spider, path, meta)
        dfd = threads.deferToThread(self._write, k, obj, headers,
                                    policy='private')
        dfd.addCallback(lambda r, k: k.name, k)
        return dfd

    def _get_existing_key(self, key_name):
        # TODO: use deferred?
        b = self._get_bucket()
        k = b.get_key(key_name)
        return k

    def generate_url(self, key_name, expires_in=300,  query_auth=True,
                     force_http=True):
        # TODO: use deferred?
        k = self._get_existing_key(key_name)
        url = k.generate_url(expires_in=expires_in, query_auth=query_auth,
                             force_http=force_http)
        return url

def errback(failure, item):
    item['errback_failure'] = failure.getTraceback()
    return item
