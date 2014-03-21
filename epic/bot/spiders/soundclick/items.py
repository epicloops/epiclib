# -*- coding: utf-8 -*-
'''
Soundclick-specific items
'''
from __future__ import unicode_literals

from scrapy.item import Field

from epic.bot.items import TrackItem


class SoundclickTrackItem(TrackItem):
    '''Soundclick-specific Track item.'''

    soundclick_artist_id = Field()
    soundclick_songid = Field()
    soundclick_commercial = Field()
    soundclick_modifications = Field()
    soundclick_download_url = Field()
    soundclick_xml_url = Field()
