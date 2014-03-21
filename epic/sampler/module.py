# -*- coding: utf-8 -*-
'''
Salt module that plits tracks from epicbot into samples based on cuesheets and
saves the results to S3.
'''
import logging
import os
import shutil
import subprocess
import datetime
import math

import salt.client
import salt.utils.event
from salt.utils.event import tagify as _tagify

from epic import config
from epic.db import session_maker
from epic.db.models import DeclarativeBase, SamplerErrors
from epic import s3


log = logging.getLogger(__name__)


def __virtual__():
    if config.read_config():
        return True
    return False

def _partition(lst, n):
    '''
    Partition a list into n lists.

    :param lst: List to partition.
    :param n: Number of partitions.
    '''
    division = len(lst) / float(n)
    ret = []
    for i in xrange(n):
        start = int(round(division*i))
        end = int(round(division*(i+1)))
        ret.append(lst[start:end])
    return ret

def _write_cue(track_dir, samples, sample_name):
    cue = [
        'PERFORMER " "',
        'TITLE " "',
        'FILE "track.mp3" MP3',
    ]
    for sample in samples:
        mins, secs = divmod(sample.start, 60)
        frame = math.floor((secs % 1)/.013333)
        secs = math.floor(secs)
        entry = [
            '  TRACK {:04d} AUDIO'.format(sample.sample_num+1),

            '    TITLE "{sn}-{i:04d}"'.format(sn=sample_name,
                                              i=sample.sample_num+1),

            '    PERFORMER " "',

            '    INDEX 01 {mins:02.0f}:{secs:02.0f}:'
            '{frame:02.0f}'.format(mins=mins, secs=secs, frame=frame),
        ]
        cue += entry

    fname = os.path.join(track_dir, '{}.cue'.format(sample_name))
    with open(fname, 'w') as f:
        f.write('\n'.join(cue))
        log.info('Wrote %s', fname)

    return fname

def run(crawl_start, spider,
        sampler_start='{:%Y-%m-%dT%H-%M-%S}'.format(datetime.datetime.now()),
        minions=1, offset=0, qty=-1):
    '''
    Run sampler.

    CLI Example::

    .. code-block:: bash

        salt 'sampler-*' epicsampler.run crawl_start=2014-01-20T01-34-37 spider=soundclick
    '''
    # define some common vars
    bot_dir = '/'.join(['bot', crawl_start, spider])
    temp_dir = '/tmp/epicsampler'
    sampler_dir = '/'.join(['sampler', crawl_start, spider, sampler_start])

    # init event data to send progress updates to master
    update_tag = _tagify(['monitor','update'], base='epicsampler')
    ret = {
        'assigned_tracks': 0,
        'downloaded_tracks': 0,
        'processed_tracks': 0,
        'sections': 0,
        'bars': 0,
        'beats': 0,
        'errors': 0,
        'complete': 0,
    }

    log.info('Querying S3 and calculating workload.')
    tracks_all = (k for k in s3.list(bot_dir))

    # limit track list based on offset and qty params
    tracks_subset = []
    for i, k in enumerate(tracks_all):
        if i >= offset and (qty<1 or i < (offset)+qty):
            tracks_subset.append(k)

    # partition track list if more than 1 minion is being used
    # and select partition that corresponds to this monion's id
    if minions > 1:
        partitions = _partition(tracks_subset, minions)
        minion_id = int(__grains__['id'].split('-')[1])
        tracks_subset = partitions[minion_id]
    ret['assigned_tracks'] = len(tracks_subset)

    # clear temp dir
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
        log.info('Removed %s', temp_dir)
    os.makedirs(temp_dir)
    log.info('Created %s', temp_dir)

    Session = session_maker()
    for k in tracks_subset:
        log.info('Processing %s', k)
        track_id = k.name.split('/')[3]
        track_dir = os.path.join(temp_dir, track_id)

        track_file = s3.get(k, os.path.join(track_dir, 'track.mp3'))
        ret['downloaded_tracks'] += 1
        __salt__['event.fire_master'](ret, update_tag)

        for sample_name in config.PROCESS_SAMPLES:

            # make sample_dir
            sample_dir = os.path.join(track_dir, sample_name)
            if not os.path.exists(sample_dir):
                os.makedirs(sample_dir)

            log.info('Querying database for %s data.', sample_name)
            session = Session()
            table = DeclarativeBase.metadata.tables[sample_name]
            samples = session.query(table).\
                        filter_by(track_id=track_id, crawl_start=crawl_start).\
                        order_by(table.c.start).all()
            session.close()
            cue_file = _write_cue(track_dir, samples, sample_name)

            # split track in track_dir based on cue_file and write the samples
            # to sample_dir
            cmd = 'mp3splt -n -x -c {0} -d {1} -o @n4 {2}'.format(cue_file,
                                                                  sample_dir,
                                                                  track_file)
            try:
                subprocess.check_output(cmd, shell=True)
            except subprocess.CalledProcessError, e:
                log.warning('\n\n'.join(['Split error:',
                                         'CMD:\n%s',
                                         'RETURNCODE:\n%s',
                                         'OUTPUT:\n %s',]),
                            e.cmd,
                            e.returncode,
                            e.output)

                session = Session()
                try:
                    session.add(SamplerErrors(track_id=track_id,
                                              crawl_start=crawl_start,
                                              sampler_start=sampler_start,
                                              cmd=e.cmd,
                                              returncode=e.returncode,
                                              output=e.output))
                except:
                    session.rollback()
                    raise
                else:
                    session.commit()
                finally:
                    session.close()
                    ret['errors'] += 1
                    __salt__['event.fire_master'](ret, update_tag)
                break

            # upload sample files to s3
            for i, fname in enumerate(os.listdir(sample_dir)):
                kname = '/'.join([sampler_dir, track_id, sample_name, fname])
                s3.set(kname, os.path.join(sample_dir, fname))
                try:
                    ret[sample_name] += 1
                except KeyError:
                    ret[sample_name] = 0
                # Only send events every 10
                # Sending less events seems to avoid "Bad file descriptor"
                # error from 0mq
                if i % 10 == 0:
                    __salt__['event.fire_master'](ret, update_tag)

            log.info('%s have been split and uploaded for %s',
                     sample_name, track_id)

        log.info('%s track processed.', track_id)
        ret['processed_tracks'] += 1
        __salt__['event.fire_master'](ret, update_tag)

    ret['complete'] = 1
    salt.output.display_output(ret, 'yaml', __opts__)
    __salt__['event.fire_master'](ret, update_tag)
    ret['_stamp'] = datetime.datetime.now().isoformat('_')
    return ret
