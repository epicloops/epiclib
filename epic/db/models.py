'''
Models.
'''
import logging

from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    Text,
    PickleType
)
from sqlalchemy.ext.declarative import declarative_base


log = logging.getLogger(__name__)


DeclarativeBase = declarative_base()

class Tracks(DeclarativeBase):

    __tablename__ = "tracks"

    track_id = Column('track_id', String(32), primary_key=True)
    crawl_start = Column('crawl_start', String(50), primary_key=True)
    artist = Column('artist', String(500))
    artist_page_url = Column('artist_page_url', String(500))
    track_url = Column('track_url', String(500))
    s3_key = Column('s3_key', String(500))
    description = Column('description', String(500))
    download_flag = Column('download_flag', String(1))
    dropped_item_exception = Column('dropped_item_exception', String(5000))
    errback_failure = Column('errback_failure', Text)
    genre = Column('genre', String(500))
    license_url = Column('license_url', String(500))
    origin_page_url = Column('origin_page_url', String(500))
    sub_genre = Column('sub_genre', String(500))
    title = Column('title', String(500))
    track_page_url = Column('track_page_url', String(500))
    echonest_acousticness = Column('echonest_acousticness', Float)
    echonest_album = Column('echonest_album', String(500))
    echonest_analysis_channels = Column('echonest_analysis_channels', Float)
    echonest_analysis_sample_rate = Column('echonest_analysis_sample_rate',
                                           Float)
    echonest_analysis_time = Column('echonest_analysis_time', Float)
    echonest_analysis_url = Column('echonest_analysis_url', String(500))
    echonest_analyzer_version = Column('echonest_analyzer_version', String(20))
    echonest_artist = Column('echonest_artist', String(500))
    echonest_artist_id = Column('echonest_artist_id', String(500))
    echonest_audio_md5 = Column('echonest_audio_md5', String(32))
    echonest_bars = Column('echonest_bars', String(500))
    echonest_beats = Column('echonest_beats', String(500))
    echonest_bitrate = Column('echonest_bitrate', Float)
    echonest_cache = Column('echonest_cache', PickleType)
    echonest_code_version = Column('echonest_code_version', Float)
    echonest_codestring = Column('echonest_codestring', Text)
    echonest_danceability = Column('echonest_danceability', Float)
    echonest_decoder = Column('echonest_decoder', String(20))
    echonest_detailed_status = Column('echonest_detailed_status', String(20))
    echonest_duration = Column('echonest_duration', Float)
    echonest_echoprint_version = Column('echonest_echoprint_version', Float)
    echonest_echoprintstring = Column('echonest_echoprintstring', Text)
    echonest_end_of_fade_in = Column('echonest_end_of_fade_in', Float)
    echonest_energy = Column('echonest_energy', Float)
    echonest_filename = Column('echonest_filename', String(500))
    echonest_genre = Column('echonest_genre', String(500))
    echonest_id = Column('echonest_id', String(50))
    echonest_key = Column('echonest_key', Integer)
    echonest_key_confidence = Column('echonest_key_confidence', Float)
    echonest_liveness = Column('echonest_liveness', Float)
    echonest_loudness = Column('echonest_loudness', Float)
    echonest_md5 = Column('echonest_md5', String(32))
    echonest_mode = Column('echonest_mode', Integer)
    echonest_mode_confidence = Column('echonest_mode_confidence', Float)
    echonest_num_samples = Column('echonest_num_samples', Float)
    echonest_offset_seconds = Column('echonest_offset_seconds', Float)
    echonest_platform = Column('echonest_platform', String(50))
    echonest_rhythm_version = Column('echonest_rhythm_version', Float)
    echonest_rhythmstring = Column('echonest_rhythmstring', Text)
    echonest_sample_md5 = Column('echonest_sample_md5', String(32))
    echonest_samplerate = Column('echonest_samplerate', Float)
    echonest_seconds = Column('echonest_seconds', Float)
    echonest_sections = Column('echonest_sections', String(500))
    echonest_segments = Column('echonest_segments', String(500))
    echonest_song_id = Column('echonest_song_id', String(50))
    echonest_speechiness = Column('echonest_speechiness', Float)
    echonest_start_of_fade_out = Column('echonest_start_of_fade_out', Float)
    echonest_status = Column('echonest_status', String(50))
    echonest_status_code = Column('echonest_status_code', Float)
    echonest_synch_version = Column('echonest_synch_version', Float)
    echonest_synchstring = Column('echonest_synchstring', Text)
    echonest_tatums = Column('echonest_tatums', String(500))
    echonest_tempo = Column('echonest_tempo', Float)
    echonest_tempo_confidence = Column('echonest_tempo_confidence', Float)
    echonest_time_signature = Column('echonest_time_signature', Float)
    echonest_time_signature_confidence = Column(
                                'echonest_time_signature_confidence', Float)
    echonest_timestamp = Column('echonest_timestamp', Float)
    echonest_title = Column('echonest_title', String(500))
    echonest_valence = Column('echonest_valence', Float)

class Sections(DeclarativeBase):

    __tablename__ = "sections"

    track_id = Column('track_id', String(32), primary_key=True)
    crawl_start = Column('crawl_start', String(50), primary_key=True)
    sample_num = Column('sample_num', Integer, primary_key=True)
    confidence = Column('confidence', Float)
    duration = Column('duration', Float)
    key = Column('key', Integer)
    key_confidence = Column('key_confidence', Float)
    loudness = Column('loudness', Float)
    mode = Column('mode', Integer)
    mode_confidence = Column('mode_confidence', Float)
    start = Column('start', Float)
    tempo = Column('tempo', Float)
    tempo_confidence = Column('tempo_confidence', Float)
    time_signature = Column('time_signature', Integer)
    time_signature_confidence = Column('time_signature_confidence', Float)

class Bars(DeclarativeBase):

    __tablename__ = "bars"

    track_id = Column('track_id', String(32), primary_key=True)
    crawl_start = Column('crawl_start', String(50), primary_key=True)
    sample_num = Column('sample_num', Integer, primary_key=True)
    confidence = Column('confidence', Float)
    duration = Column('duration', Float)
    start = Column('start', Float)

class Beats(DeclarativeBase):

    __tablename__ = "beats"

    track_id = Column('track_id', String(32), primary_key=True)
    crawl_start = Column('crawl_start', String(50), primary_key=True)
    sample_num = Column('sample_num', Integer, primary_key=True)
    confidence = Column('confidence', Float)
    duration = Column('duration', Float)
    start = Column('start', Float)

class Tatums(DeclarativeBase):

    __tablename__ = "tatums"

    track_id = Column('track_id', String(32), primary_key=True)
    crawl_start = Column('crawl_start', String(50), primary_key=True)
    sample_num = Column('sample_num', Integer, primary_key=True)
    confidence = Column('confidence', Float)
    duration = Column('duration', Float)
    start = Column('start', Float)

class Segments(DeclarativeBase):

    __tablename__ = "segments"

    track_id = Column('track_id', String(32), primary_key=True)
    crawl_start = Column('crawl_start', String(50), primary_key=True)
    sample_num = Column('sample_num', Integer, primary_key=True)
    confidence = Column('confidence', Float)
    duration = Column('duration', Float)
    loudness_max = Column('loudness_max', Float)
    loudness_max_time = Column('loudness_max_time', Float)
    loudness_start = Column('loudness_start', Float)
    pitches = Column('pitches', String(500))
    start = Column('start', Float)
    timbre = Column('timbre', String(500))

class Dropped(DeclarativeBase):

    __tablename__ = "dropped"

    track_id = Column('track_id', String(32), primary_key=True)
    crawl_start = Column('crawl_start', String(50), primary_key=True)
    artist = Column('artist', String(500))
    artist_page_url = Column('artist_page_url', String(500))
    track_url = Column('track_url', String(500))
    s3_key = Column('s3_key', String(500))
    description = Column('description', String(500))
    download_flag = Column('download_flag', String(1))
    dropped_item_exception = Column('dropped_item_exception', String(5000))
    errback_failure = Column('errback_failure', Text)
    genre = Column('genre', String(500))
    license_url = Column('license_url', String(500))
    origin_page_url = Column('origin_page_url', String(500))
    sub_genre = Column('sub_genre', String(500))
    title = Column('title', String(500))
    track_page_url = Column('track_page_url', String(500))
    echonest_acousticness = Column('echonest_acousticness', Float)
    echonest_album = Column('echonest_album', String(500))
    echonest_analysis_channels = Column('echonest_analysis_channels', Float)
    echonest_analysis_sample_rate = Column('echonest_analysis_sample_rate',
                                           Float)
    echonest_analysis_time = Column('echonest_analysis_time', Float)
    echonest_analysis_url = Column('echonest_analysis_url', String(500))
    echonest_analyzer_version = Column('echonest_analyzer_version', String(20))
    echonest_artist = Column('echonest_artist', String(500))
    echonest_artist_id = Column('echonest_artist_id', String(500))
    echonest_audio_md5 = Column('echonest_audio_md5', String(32))
    echonest_bars = Column('echonest_bars', String(500))
    echonest_beats = Column('echonest_beats', String(500))
    echonest_bitrate = Column('echonest_bitrate', Float)
    echonest_cache = Column('echonest_cache', PickleType)
    echonest_code_version = Column('echonest_code_version', Float)
    echonest_codestring = Column('echonest_codestring', Text)
    echonest_danceability = Column('echonest_danceability', Float)
    echonest_decoder = Column('echonest_decoder', String(20))
    echonest_detailed_status = Column('echonest_detailed_status', String(20))
    echonest_duration = Column('echonest_duration', Float)
    echonest_echoprint_version = Column('echonest_echoprint_version', Float)
    echonest_echoprintstring = Column('echonest_echoprintstring', Text)
    echonest_end_of_fade_in = Column('echonest_end_of_fade_in', Float)
    echonest_energy = Column('echonest_energy', Float)
    echonest_filename = Column('echonest_filename', String(500))
    echonest_genre = Column('echonest_genre', String(500))
    echonest_id = Column('echonest_id', String(50))
    echonest_key = Column('echonest_key', Integer)
    echonest_key_confidence = Column('echonest_key_confidence', Float)
    echonest_liveness = Column('echonest_liveness', Float)
    echonest_loudness = Column('echonest_loudness', Float)
    echonest_md5 = Column('echonest_md5', String(32))
    echonest_mode = Column('echonest_mode', Integer)
    echonest_mode_confidence = Column('echonest_mode_confidence', Float)
    echonest_num_samples = Column('echonest_num_samples', Float)
    echonest_offset_seconds = Column('echonest_offset_seconds', Float)
    echonest_platform = Column('echonest_platform', String(50))
    echonest_rhythm_version = Column('echonest_rhythm_version', Float)
    echonest_rhythmstring = Column('echonest_rhythmstring', Text)
    echonest_sample_md5 = Column('echonest_sample_md5', String(32))
    echonest_samplerate = Column('echonest_samplerate', Float)
    echonest_seconds = Column('echonest_seconds', Float)
    echonest_sections = Column('echonest_sections', String(500))
    echonest_segments = Column('echonest_segments', String(500))
    echonest_song_id = Column('echonest_song_id', String(50))
    echonest_speechiness = Column('echonest_speechiness', Float)
    echonest_start_of_fade_out = Column('echonest_start_of_fade_out', Float)
    echonest_status = Column('echonest_status', String(50))
    echonest_status_code = Column('echonest_status_code', Float)
    echonest_synch_version = Column('echonest_synch_version', Float)
    echonest_synchstring = Column('echonest_synchstring', Text)
    echonest_tatums = Column('echonest_tatums', String(500))
    echonest_tempo = Column('echonest_tempo', Float)
    echonest_tempo_confidence = Column('echonest_tempo_confidence', Float)
    echonest_time_signature = Column('echonest_time_signature', Float)
    echonest_time_signature_confidence = Column(
                                'echonest_time_signature_confidence', Float)
    echonest_timestamp = Column('echonest_timestamp', Float)
    echonest_title = Column('echonest_title', String(500))
    echonest_valence = Column('echonest_valence', Float)

class SamplerErrors(DeclarativeBase):

    __tablename__ = "sampler_errors"

    track_id = Column('track_id', String(32), primary_key=True)
    crawl_start = Column('crawl_start', String(50), primary_key=True)
    sampler_start = Column('sampler_start', String(50), primary_key=True)
    cmd = Column('cmd', String(500), primary_key=True)
    returncode = Column('returncode', String(20))
    output = Column('output', Text)
