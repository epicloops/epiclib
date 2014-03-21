# -*- coding: utf-8 -*-
'''
Download track from source and upload to s3.
'''
from __future__ import unicode_literals

from twisted.internet import threads

from scrapy import log
from scrapy.http import Request
from scrapy.exceptions import DropItem

from epic import s3


class TrackPipelineDropItem(DropItem):

    pass


class TrackPipeline(object):

    def __init__(self, crawler):
        self.crawler = crawler
        self.settings = crawler.settings

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_item(self, item, spider):

        try:
            request = Request(url=item.get('track_url', None))
        except TypeError:
            msg = ('{cls}: Missing field: track_url'.format(
                                                cls=self.__class__.__name__))
            raise TrackPipelineDropItem(msg)

        request.meta['handle_httpstatus_all'] = True

        dfd = self.crawler.engine.download(request, spider)
        dfd.addCallbacks(
            callback=self.dl_success, callbackArgs=(request, item, spider),
            errback=self.dl_fail, errbackArgs=(request, item, spider))

        return dfd

    def dl_fail(self, failure, request, item, spider):

        referer = request.headers.get('Referer')

        msg = ('{cls}: Unknown error downloading file from {request} referred'
               ' in {referer}: {exception}'.format(cls=self.__class__.__name__,
                                                   exception=failure.value,
                                                   request=request,
                                                   referer=referer))
        raise TrackPipelineDropItem(msg)

    def dl_success(self, response, request, item, spider):

        referer = request.headers.get('Referer')

        if response.status != 200:
            msg = ('{cls}: Got ({status}) downloading {request} referred in '
                   '{referer}'.format(cls=self.__class__.__name__,
                                      status=response.status,
                                      request=request, referer=referer))
            raise TrackPipelineDropItem(msg)

        if not response.body:
            msg = ('Empty response body: {request} referred in '
                   '<{referer}>'.format(request=request, referer=referer))
            raise TrackPipelineDropItem(msg)

        log.msg(format='Downloaded: %(request)s referred in <%(referer)s>',
                level=log.DEBUG, spider=spider, request=request,
                referer=referer)

        spider.crawler.stats.inc_value(
            '{}/file_download_count'.format(self.__class__.__name__),
            spider=spider)

        key_name = 'bot/{0}/{1}/{2}/track.mp3'.format(item['crawl_start'],
                                                      spider.name,
                                                      item['track_id'])

        dfd = threads.deferToThread(s3.set, key_name, response.body)
        dfd.addCallback(self.ul_success, item, spider)

        return dfd

    def ul_success(self, key, item, spider):

        item['s3_key'] = key.name

        spider.crawler.stats.inc_value(
            '{}/file_upload_count'.format(self.__class__.__name__),
            spider=spider)

        log.msg(format='Uploaded: <%(url)s> uploaded to <%(key_name)s>',
                level=log.DEBUG, spider=spider, url=item['track_page_url'],
                key_name=item['s3_key'])

        return item
