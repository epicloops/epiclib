# -*- coding: utf-8 -*-
'''
Populate items with data from echonest api.
'''
from __future__ import unicode_literals

from pyechonest import config as econfig
from pyechonest import track as etrack

from twisted.internet import threads

from scrapy import log, signals
from scrapy.exceptions import DropItem

from epic.utils.fms import S3FM


class EchonestPipelineDropItem(DropItem):

    pass


class EchonestPipeline(object):

    def __init__(self, crawler):
        self.crawler = crawler
        self.stats = crawler.stats
        self.settings = crawler.settings
        self.s3 = None

    @classmethod
    def from_crawler(cls, crawler):
        ext = cls(crawler)
        crawler.signals.connect(ext.spider_opened, signals.spider_opened)
        return ext

    def spider_opened(self, spider):
        self.s3 = S3FM(self.stats.get_value('crawl_id'))

    def process_item(self, item, spider):

        def _api_call(url):
            track = etrack.track_from_url(url)
            track.get_analysis()
            return track

        def _populate_fields(track, self, item, spider):
            for data in [ track.__dict__, track.__dict__['meta'] ]:
                for k, v in data.items():
                    if 'echonest_{}'.format(k) in item.fields:
                        item['echonest_{}'.format(k)] = v

            spider.crawler.stats.inc_value(
                '{}/echonest_count'.format(self.__class__.__name__),
                spider=spider)

            log.msg(format='Echonest: <%(key_name)s> fields populated',
                    level=log.DEBUG, spider=spider,
                    key_name=item['s3_key'])

            return item

        econfig.ECHO_NEST_API_KEY = self.settings.get('ECHONEST_API_KEY')

        log.msg(format='Echonest: <%(key_name)s> posting to Echonest API',
                level=log.DEBUG, spider=spider,
                key_name=item['s3_key'])

        url = self.s3.generate_url(item['s3_key'])

        dfd = threads.deferToThread(_api_call, url)
        dfd.addCallback(_populate_fields, self, item, spider)

        return dfd
