# -*- coding: utf-8 -*-
'''
Common spider utility functions.
'''
from __future__ import unicode_literals


def errback(failure, item):
    item['errback_failure'] = failure.getTraceback()
    return item
