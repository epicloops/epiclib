# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from scrapy.exceptions import DropItem


class DuplicateDropItem(DropItem):

    pass

class DuplicatesPipeline(object):

    def __init__(self):
        self.keys_seen = set()

    def process_item(self, item, spider):

        if item['crawl_key'] in self.keys_seen:
            raise DuplicateDropItem("{cls}: {ck}".format(
                                                cls=self.__class__.__name__,
                                                ck=item['crawl_key']))
        else:
            self.keys_seen.add(item['crawl_key'])
            return item


class CCFilterDropItem(DropItem):

    pass

class CCFilterPipeline(object):

    def process_item(self, item, spider):

        cc_urls = [
            'http://creativecommons.org/licenses/by-nc-sa/2.0/',
            'http://creativecommons.org/licenses/by-nc/2.0/',
            'http://creativecommons.org/licenses/by-sa/2.0/',
            'http://creativecommons.org/licenses/by/2.0/',
        ]

        if item.get('license_url', None) not in cc_urls:
            raise CCFilterDropItem('Improper license.')
        elif item.get('download_flag', None) != 'Y':
            raise CCFilterDropItem('No free download.')
        elif not item.get('origin_url', None):
            raise CCFilterDropItem('No origin_url. Needed for licensing.')
        elif not item.get('artist_url', None):
            raise CCFilterDropItem('No artist_url. Needed for licensing.')
        elif not item.get('track_url', None):
            raise CCFilterDropItem('No track url. Needed for licensing.')

        return item
