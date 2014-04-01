# -*- coding: utf-8 -*-
'''
Splits tracks from epic.bot into samples and saves the results to S3.
'''
import logging
import os
import subprocess
import json
import time

from epic.db.models import Track, Sample, SamplerError
from epic.utils.fms import LocalFM, S3FM
from epic.utils import queue, Cue


log = logging.getLogger(__name__)


__version__ = '0.1.0'


class Manager(object):

    def __init__(self, session):
        self.queue = queue.create()
        self.session = session
        self.s3 = S3FM()
        self.fm = LocalFM()

    def run(self):
        while True:
            msg = self.queue.read()
            if not msg:
                log.info('Queue empty. Checking again in 15 seconds.')
                time.sleep(15)
                continue

            item = json.loads(msg.get_body())
            log.info('Processing %s', item['track_id'])

            track = self.session.query(Track).\
                        filter_by(track_id=item['track_id'],
                                  crawl_id=item['crawl_id']).one()

            self.fm.purge()
            self.s3.crawl_id = track.crawl_id

            track_file = self.s3.get(track.s3_key,
                                     self.fm.abspath('track.mp3'))

            samplers = []
            for sample_type in Sample.types_to_process():
                samplers.append(Sampler(self.session, track, track_file,
                                        sample_type))

            for sampler in samplers:
                sampler.run()


            log.info('%s track processed.', track.track_id)
            track.processed = True
            try:
                self.session.commit()
            except:
                self.session.rollback()
                raise

            self.queue.delete_message(msg)


class Sampler(object):

    def __init__(self, session, track, track_file, sample_type):
        self.session = session

        self.track = track
        self.track_id = self.track.track_id
        self.track_file = track_file

        self.s3 = S3FM(self.track.crawl_id)
        self.fm = LocalFM()

        self.sample_type = sample_type
        self.sample_dir = self.fm.mkdir(self.sample_type)
        self.samples = self.track.samples.\
                                filter_by(sample_type=self.sample_type).all()

        if self.samples:
            self.cue_file = self.fm.write('{}.cue'.format(self.sample_type),
                                          str(Cue(self.samples)))

    def run(self):
        if not self.samples:
            return

        try:
            self._sample()
        except subprocess.CalledProcessError:
            return
        else:
            self._upload()

    def _sample(self):
        cmd = 'mp3splt -n -x -c {0} -d {1} -o @n4 {2}'.format(self.cue_file,
                                                              self.sample_dir,
                                                              self.track_file)
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

            self.track.errors.append(SamplerError(cmd=e.cmd,
                                                  returncode=e.returncode,
                                                  output=e.output))
            try:
                self.session.commit()
            except:
                self.session.rollback()
                raise
            raise

    def _upload(self):

        sample_files = sorted(os.listdir(self.sample_dir))

        for i, fname in enumerate(sample_files):
            sample = self.samples[i]
            key_name = '/'.join([self.track_id,
                                 '{}s'.format(self.sample_type),
                                 fname])
            absfname = os.path.join(self.sample_dir, fname)
            self.s3.set_from_filename(key_name, absfname)
            sample.processed = True

            # Batch updates to db every 50 samples and the last sample
            if i != 0 and (i % 50 == 0 or i == len(sample_files)-1):
                try:
                    self.session.commit()
                except:
                    self.session.rollback()
                    raise


def main(session, *args, **kwargs):
    Manager(session).run()
