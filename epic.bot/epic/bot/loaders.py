# -*- coding: utf-8 -*-
'''
Base item loaders.
'''
from __future__ import unicode_literals

import urllib2

from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import Identity, TakeFirst, MapCompose


class TrackItemLoader(ItemLoader):

    default_input_processor = Identity()
    default_output_processor = TakeFirst()

    origin_page_url_in = MapCompose(lambda u: u.decode('ascii'))

    description_in = MapCompose(lambda s: s.strip())

    track_page_url_in = MapCompose(lambda u: u.decode('ascii'))

    track_url_in = MapCompose(urllib2.unquote)
