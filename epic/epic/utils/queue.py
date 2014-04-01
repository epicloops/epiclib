# -*- coding: utf-8 -*-
'''
Misc sqs fucntions.
'''
import logging

from boto import sqs

from epic import config


log = logging.getLogger(__name__)


def get_conn():
    return sqs.connect_to_region(
        config.AWS_REGION,
        aws_access_key_id=config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY)

def create():
    conn = get_conn()
    return conn.create_queue('epic', 300)
