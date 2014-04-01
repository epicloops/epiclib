# -*- coding: utf-8 -*-
'''
Models.
'''
import logging

from sqlalchemy import (
    Column,
    DateTime,
    Boolean,
    Integer,
    Float,
    String,
    Text,
    PickleType,
    ForeignKey
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base, declared_attr

from epic import config


log = logging.getLogger(__name__)


class DeclarativeBase(object):

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


Base = declarative_base(cls=DeclarativeBase)


class SingleTableMixin(object):

    __tablename__ = None


class Track(Base):

    pid = Column(Integer, primary_key=True)
    track_id = Column(String(32))
    crawl_id = Column(String(50))
    spider = Column(String(50))
    spider_start = Column(DateTime)
    artist = Column(String(500))
    artist_page_url = Column(String(500))
    track_url = Column(String(500))
    s3_key = Column(String(500))
    description = Column(String(500))
    download_flag = Column(Boolean, default=False)
    dropped_item_flag = Column(Boolean, default=False)
    errback_failure = Column(Text)
    genre = Column(String(500))
    license_url = Column(String(500))
    origin_page_url = Column(String(500))
    sub_genre = Column(String(500))
    title = Column(String(500))
    track_page_url = Column(String(500))
    echonest_acousticness = Column(Float)
    echonest_album = Column(String(500))
    echonest_analysis_channels = Column(Float)
    echonest_analysis_sample_rate = Column(Float)
    echonest_analysis_time = Column(Float)
    echonest_analysis_url = Column(String(500))
    echonest_analyzer_version = Column(String(20))
    echonest_artist = Column(String(500))
    echonest_artist_id = Column(String(500))
    echonest_audio_md5 = Column(String(32))
    echonest_bitrate = Column(Float)
    echonest_cache = Column(PickleType)
    echonest_code_version = Column(Float)
    echonest_codestring = Column(Text)
    echonest_danceability = Column(Float)
    echonest_decoder = Column(String(20))
    echonest_detailed_status = Column(String(20))
    echonest_duration = Column(Float)
    echonest_echoprint_version = Column(Float)
    echonest_echoprintstring = Column(Text)
    echonest_end_of_fade_in = Column(Float)
    echonest_energy = Column(Float)
    echonest_filename = Column(String(500))
    echonest_genre = Column(String(500))
    echonest_id = Column(String(50))
    echonest_key = Column(Integer)
    echonest_key_confidence = Column(Float)
    echonest_liveness = Column(Float)
    echonest_loudness = Column(Float)
    echonest_md5 = Column(String(32))
    echonest_mode = Column(Integer)
    echonest_mode_confidence = Column(Float)
    echonest_num_samples = Column(Float)
    echonest_offset_seconds = Column(Float)
    echonest_platform = Column(String(50))
    echonest_rhythm_version = Column(Float)
    echonest_rhythmstring = Column(Text)
    echonest_sample_md5 = Column(String(32))
    echonest_samplerate = Column(Float)
    echonest_seconds = Column(Float)
    echonest_song_id = Column(String(50))
    echonest_speechiness = Column(Float)
    echonest_start_of_fade_out = Column(Float)
    echonest_status = Column(String(50))
    echonest_status_code = Column(Float)
    echonest_synch_version = Column(Float)
    echonest_synchstring = Column(Text)
    echonest_tempo = Column(Float)
    echonest_tempo_confidence = Column(Float)
    echonest_time_signature = Column(Float)
    echonest_time_signature_confidence = Column(Float)
    echonest_timestamp = Column(Float)
    echonest_title = Column(String(500))
    echonest_valence = Column(Float)
    processed = Column(Boolean, default=False)

    samples = relationship('Sample', lazy='dynamic', backref='track',
                        order_by='Sample.sample_type, Sample.sample_num.asc()',
                        cascade='all, delete-orphan')

    errors = relationship('ProcessingError', backref='track',
                        order_by='ProcessingError.error_type',
                        cascade='all, delete-orphan')

    __mapper_args__ = {
        'polymorphic_identity': False,
        'polymorphic_on': dropped_item_flag
    }


class DroppedTrack(Track):

    pid = Column(Integer, primary_key=True)
    track_pid = Column(Integer, ForeignKey('track.pid'))
    dropped_item_exception = Column(String(5000))

    __mapper_args__ = {
        'polymorphic_identity': True,
    }


class Sample(Base):

    pid = Column(Integer, primary_key=True)
    track_pid = Column(Integer, ForeignKey('track.pid'))
    sample_type = Column(String(50))
    sample_num = Column(Integer)
    start = Column(Float)
    confidence = Column(Float)
    duration = Column(Float)
    processed = Column(Boolean, default=False)

    __mapper_args__ = {
        'polymorphic_identity': 'sample',
        'polymorphic_on': sample_type,
        'order_by': [track_pid.asc(), sample_num.asc()]
    }

    @classmethod
    def types_to_process(cls):
        sample_types = []
        for poly_ident in cls.__mapper__.polymorphic_map:
            if '{}s'.format(poly_ident) in [s.lower() for s in config.SAMPLES]:
                sample_types.append(poly_ident)
        return sample_types



class Section(Sample, Base):

    pid = Column(Integer, ForeignKey('sample.pid'), primary_key=True)
    key = Column(Integer)
    key_confidence = Column(Float)
    loudness = Column(Float)
    mode = Column(Integer)
    mode_confidence = Column(Float)
    tempo = Column(Float)
    tempo_confidence = Column(Float)
    time_signature = Column(Integer)
    time_signature_confidence = Column(Float)

    __mapper_args__ = {
        'polymorphic_identity': 'section',
    }

    __scrapy_field__ = 'echonest_sections'


class Bar(SingleTableMixin, Sample, Base):

    __mapper_args__ = {
        'polymorphic_identity': 'bar',
    }

    __scrapy_field__ = 'echonest_bars'


class Beat(SingleTableMixin, Sample, Base):

    __mapper_args__ = {
        'polymorphic_identity': 'beat',
    }

    __scrapy_field__ = 'echonest_beats'


class Tatum(SingleTableMixin, Sample, Base):

    __mapper_args__ = {
        'polymorphic_identity': 'tatum',
    }

    __scrapy_field__ = 'echonest_tatums'


class Segment(Sample, Base):

    pid = Column(Integer, ForeignKey('sample.pid'), primary_key=True)
    loudness_start = Column(Float)
    loudness_end = Column(Float)
    loudness_max = Column(Float)
    loudness_max_time = Column(Float)
    pitches = Column(String(500))
    timbre = Column(String(500))

    __mapper_args__ = {
        'polymorphic_identity': 'segment',
    }

    __scrapy_field__ = 'echonest_segments'


class ProcessingError(Base):

    pid = Column(Integer, primary_key=True)
    track_pid = Column(Integer, ForeignKey('track.pid'))
    error_type = Column(String(50))
    cmd = Column(String(500))
    returncode = Column(String(20))
    output = Column(Text)

    __mapper_args__ = {
        'polymorphic_identity': 'general',
        'polymorphic_on': error_type,
        'order_by': [track_pid.asc(), error_type]
    }


class SamplerError(SingleTableMixin, ProcessingError, Base):

    __mapper_args__ = {
        'polymorphic_identity': 'sampler',
    }
