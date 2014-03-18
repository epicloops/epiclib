'''
Analyzes the results of epicbot and epicsampler.
'''
import logging

from sqlalchemy import select

from epic.models import session, Tracks


log = logging.getLogger(__name__)


def avg_confidence(name, *args, **kwargs):
    '''Rank tracks by avg confidence of `name` param.


    '''
    pass
