# -*- coding: utf-8 -*-
'''
Base items.
'''
from __future__ import unicode_literals

from scrapy.item import Item, Field

from epic.db.models import Tracks

class TrackItem(Item):
    '''Base Track item.'''

    fields = {}
    for column in Tracks.__table__.columns:
        fields[column.name] = Field()
