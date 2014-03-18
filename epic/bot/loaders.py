# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import urllib2

from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import Identity, TakeFirst, MapCompose


class TrackItemLoader(ItemLoader):

    default_input_processor = Identity()
    default_output_processor = TakeFirst()

    origin_url_in = MapCompose(lambda u: u.decode('ascii'))

    description_in = MapCompose(lambda s: s.strip())

    track_url_in = MapCompose(lambda u: u.decode('ascii'))

    data_url_in = MapCompose(urllib2.unquote)
