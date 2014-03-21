# -*- coding: utf-8 -*-
'''
Soundclick-specific loaders.
'''
from __future__ import unicode_literals

from scrapy.contrib.loader.processor import MapCompose

from epic.bot.loaders import TrackItemLoader


class SoundclickTrackItemLoader(TrackItemLoader):
    '''Soundclick-specific Track item loader.'''

    soundclick_xml_url_in = MapCompose(lambda u: u.decode('ascii'))
