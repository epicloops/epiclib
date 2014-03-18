# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from scrapy.item import Item, Field

from epic.models import Tracks

class TrackItem(Item):

    fields = {}
    for column in Tracks.__table__.columns:
        fields[column.name] = Field()
