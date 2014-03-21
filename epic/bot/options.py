# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class Options(object):
    '''Common spider options.'''

    def __init__(self, max_tracks, start_page, max_pages):
        self._max_tracks = None
        self._start_page = None
        self._max_pages = None

        self.max_tracks = max_tracks
        self.start_page = start_page
        self.max_pages = max_pages

    @property
    def max_pages(self):
        return self._max_pages

    @max_pages.setter
    def max_pages(self, value):
        if value:
            if int(value) < 1:
                raise ValueError('pages option must be 1 or greater')
            self._max_pages = int(value)
        else:
            self._max_pages = value

    @property
    def max_tracks(self):
        return self._max_tracks

    @max_tracks.setter
    def max_tracks(self, value):
        if value:
            if int(value) not in range(0, 101):
                raise ValueError('tracks option must be between 0 and 100')
            self._max_tracks = int(value)
        else:
            self._max_tracks = value

    @property
    def start_page(self):
        return self._start_page

    @start_page.setter
    def start_page(self, value):
        if value:
            if int(value) < 1:
                raise ValueError('startpage option must be 1 or greater')
            self._start_page = int(value)
        else:
            self._start_page = value

