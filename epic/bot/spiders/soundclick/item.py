# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from scrapy.item import Field

from epic.bot.items import TrackItem


class SoundclickTrackItem(TrackItem):

    soundclick_artist_id = Field()
    soundclick_songid = Field()
    soundclick_commercial = Field()
    soundclick_modifications = Field()
    soundclick_download_url = Field()
    soundclick_xml_url = Field()
