# -*- coding: utf-8 -*-
'''
Write items to queue to be read by samplers.
'''
from __future__ import unicode_literals

from scrapy import log
from scrapy.exceptions import DropItem

from boto.sqs.jsonmessage import JSONMessage

from epic.utils import queue


class QueuePipelineDropItem(DropItem):

    pass


class QueuePipeline(object):

    def __init__(self, crawler):
        self.crawler = crawler
        self.settings = crawler.settings
        self.queue = queue.create()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_item(self, item, spider):
        m = JSONMessage(body={
                'track_id': item['track_id'],
                'crawl_id': item['crawl_id'],
            })
        self.queue.write(m)
        log.msg(format='Queued: Track - %(s3_key)s',
                level=log.DEBUG, spider=spider,
                s3_key=item['s3_key'])
        return item

