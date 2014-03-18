# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from scrapy.contrib.loader.processor import MapCompose

from epic.bot.loaders import TrackItemLoader


class SoundclickTrackItemLoader(TrackItemLoader):

    soundclick_xml_url_in = MapCompose(lambda u: u.decode('ascii'))
