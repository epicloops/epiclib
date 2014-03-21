# -*- coding: utf-8 -*-
'''
Populate items with data from echonest api.
'''
from __future__ import unicode_literals

from pyechonest import config as econfig
from pyechonest import track as etrack

from twisted.internet import threads

from scrapy import log
from scrapy.exceptions import DropItem

from epic import s3


class EchonestPipelineDropItem(DropItem):

    pass


class EchonestPipeline(object):

    def __init__(self, crawler):
        self.crawler = crawler
        self.settings = crawler.settings

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_item(self, item, spider):

        def _populate_fields(self, item, spider):
            # TODO: Use deferToThread if rate limit is removed
            # Echo Nest API Error 3: 3|You are limited to 20 accesses every minute.

            # def _api_request(key):
            #     track = etrack.track_from_url(key)
            #     track.get_analysis()
            #     return track

            # def _populate_fields(track):

            #     for data in [ track.__dict__, track.__dict__['meta'] ]:
            #         for k, v in data.items():
            #             if 'echonest_{}'.format(k) in item.fields:
            #                 item['echonest_{}'.format(k)] = v

            #     return item

            # econfig.ECHO_NEST_API_KEY = self.settings.get('ECHONEST_API_KEY')

            # s3_key = self.store.generate_url(item['s3_key'])
            # dfd = threads.deferToThread(_api_request,
            #                             self.store.generate_url(s3_key))
            # dfd.addCallback(_populate_fields)

            # return dfd

            econfig.ECHO_NEST_API_KEY = self.settings.get('ECHONEST_API_KEY')

            log.msg(format='Echonest: <%(key_name)s> posting to Echonest API',
                    level=log.DEBUG, spider=spider,
                    key_name=item['s3_key'])

            s3_key = s3.generate_url(item['s3_key'])
            track = etrack.track_from_url(s3_key)

            track.get_analysis()

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

        return threads.deferToThread(_populate_fields, self, item, spider)
