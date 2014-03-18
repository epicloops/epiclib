# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from twisted.internet import threads

from scrapy import log
from scrapy.exceptions import DropItem

from epic.models import (
    session,
    Tracks,
    Sections,
    Bars,
    Beats,
    Tatums,
    Segments
)


class DbPipelineDropItem(DropItem):

    pass


class DbPipeline(object):

    def __init__(self, crawler):
        self.crawler = crawler
        self.settings = crawler.settings
        self.Session = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def open_spider(self, spider):
        self.Session = session()

    def process_item(self, item, spider):

        def _persist_item(self, item, spider):
            sample_model = {
                'sections': Sections,
                'bars': Bars,
                'beats': Beats,
                'tatums': Tatums,
                'segments': Segments,
            }
            for sample_name in self.settings.getlist('ECHONEST_SAMPLES', []):
                field = 'echonest_{}'.format(sample_name)

                for i, sample in enumerate(item[field]):
                    sample['crawl_key'] = item['crawl_key']
                    sample['crawl_start'] = item['crawl_start']
                    sample['sample_num'] = i+1

                    Model = sample_model[sample_name]

                    sample_record = dict([(k, v) for k, v in sample.items() if k in Model.__table__.columns])

                    session = self.Session()
                    try:
                        session.add(Model(**sample_record))
                    except:
                        session.rollback()
                        raise
                    else:
                        session.commit()
                        spider.crawler.stats.inc_value(
                            '{}/meta_{}_count'.format(self.__class__.__name__,
                                                      sample_name),
                            spider=spider)
                    finally:
                        session.close()

                try:
                    del item[field]
                except KeyError:
                    pass

            item_record = dict([(k, v) for k, v in item.items() if k in Tracks.__table__.columns])

            session = self.Session()
            try:
                session.add(Tracks(**item_record))
            except:
                session.rollback()
                raise
            else:
                session.commit()
                log.msg(format='Persisted: Track - %(track_url)s',
                        level=log.DEBUG, spider=spider,
                        track_url=item_record['track_url'])
                spider.crawler.stats.inc_value(
                    '{}/meta_track_count'.format(self.__class__.__name__),
                    spider=spider)
            finally:
                session.close()

            return item

        return threads.deferToThread(_persist_item, self, item, spider)
