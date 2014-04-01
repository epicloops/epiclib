# -*- coding: utf-8 -*-
'''
Base track item.
'''
from __future__ import unicode_literals

from scrapy.item import Item, Field

from epic.db.models import Track, DroppedTrack, Sample


class TrackItem(Item):
    '''Base Track item.'''

    columns = []
    for mapper in Track.__mapper__.polymorphic_iterator():
        for column in mapper.columns:
            columns.append(column.name)

    sample_classes = {}
    for k, mapper in Sample.__mapper__.polymorphic_map.items():
        if k != 'sample':
            sample_classes[k] = mapper.class_

    sample_fields = [cls.__scrapy_field__ for cls in sample_classes.values()]

    fields = {}
    for field in columns + sample_fields:
        fields[field] = Field()

    def instance(self, dropped=False):
        args = dict([(k, v) for k, v in self.items() if k in self.columns])
        if dropped:
            track = DroppedTrack(**args)
        else:
            track = Track(**args)

        for k, cls in self.sample_classes.items():
            field = cls.__scrapy_field__

            # dropped items may not have hit echonest api
            if field not in self:
                continue

            for i, sample in enumerate(self.pop(field)):
                sample['sample_num'] = i+1
                track.samples.append(cls(**sample))

        return track
