# -*- coding: utf-8 -*-
'''
Misc sqs fucntions.
'''
import logging

from boto import sqs


log = logging.getLogger(__name__)


def get_conn(aws_region, aws_access_key_id, aws_secret_access_key):

    return sqs.connect_to_region(aws_region,
                                 aws_access_key_id=aws_access_key_id,
                                 aws_secret_access_key=aws_secret_access_key)

def create(aws_region, aws_access_key_id, aws_secret_access_key):
    conn = get_conn(aws_region, aws_access_key_id, aws_secret_access_key)
    return conn.create_queue('epic', 300)
