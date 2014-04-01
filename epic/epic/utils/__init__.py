# -*- coding: utf-8 -*-
'''
Misc classes and functions.
'''
from __future__ import unicode_literals

import logging
import math


log = logging.getLogger(__name__)


class Cue(object):

    def __init__(self, samples):
        self.track = samples[0].track
        self.samples = samples

    def generate(self):
        cue = [
            'PERFORMER "{}"'.format(self.track.artist),
            'TITLE "{}"'.format(self.track.title),
            'FILE "track.mp3" MP3',
        ]
        for sample in self.samples:
            mins, secs = divmod(sample.start, 60)
            frame = math.floor((secs % 1)/.013333)
            secs = math.floor(secs)
            entry = [
                '  TRACK {:04d} AUDIO'.format(sample.sample_num),

                '    TITLE "{sn}-{i:04d}"'.format(sn=sample.sample_type,
                                                  i=sample.sample_num),

                '    PERFORMER "{}"'.format(self.track.artist),

                '    INDEX 01 {mins:02.0f}:{secs:02.0f}:'
                '{frame:02.0f}'.format(mins=mins, secs=secs, frame=frame),
            ]
            cue += entry

        return '\n'.join(cue)

    def __str__(self):

        return self.generate().encode('utf-8')

    def __repr__(self):

        return self.generate()
