# -*- coding: utf-8 -*-
'''
Manange local cache.
'''
import os
import logging
import json


log = logging.getLogger(__name__)


class Cache(object):

    def __init__(self, name):
        dirname = os.path.join(os.path.expanduser('~'), '.epic', 'cache')
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        self.path = os.path.join(dirname, name)

    def read(self):
        '''
        Attempt to read from cache.
        '''
        try:
            return json.loads(open(self.path).read())
        except IOError:
            return []

    def write(self, data):
        '''
        Write data to cache.

        :param data: Data to write to cache.
        '''
        with open(self.path, 'w') as cache:
            cache.write(json.dumps(data))

    def purge(self):
        '''
        Remove cache file.
        '''
        try:
            os.remove(self.path)
        except OSError:
            pass
