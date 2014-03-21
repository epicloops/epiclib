# -*- coding: utf-8 -*-
'''
Analyzes the results of epicbot and epicsampler.
'''
import logging

from sqlalchemy import text

from epic.db import make_engine


log = logging.getLogger(__name__)


def pro(crawl_start, limit, output=True, *args, **kwargs):
    '''Return pro tracks from a particular crawl ranked by beats confidence.'''
    engine = make_engine()
    conn = engine.connect()
    s = text('''WITH beats AS (
                    SELECT track_id, crawl_start, avg(confidence) AS confidence
                    FROM beats
                    GROUP BY track_id, crawl_start
                    ORDER BY avg(confidence) DESC
                 ),
                 bars AS (
                    SELECT track_id, crawl_start, avg(confidence) AS confidence
                    FROM bars
                    GROUP BY track_id, crawl_start
                    ORDER BY avg(confidence) DESC
                 ),
                 sections AS (
                    SELECT track_id, crawl_start, avg(confidence) AS confidence
                    FROM sections
                    GROUP BY track_id, crawl_start
                    ORDER BY avg(confidence) DESC
                 ),
                 errors AS (
                    SELECT DISTINCT track_id
                    FROM sampler_errors
                 ),
                 best AS (
                    SELECT
                        tracks.track_id,
                        tracks.crawl_start,
                        tracks.license_url,
                        beats.confidence AS beats_confidence,
                        bars.confidence AS bars_confidence,
                        sections.confidence AS sections_confidence
                    FROM
                        tracks,
                        beats,
                        bars,
                        sections
                    WHERE
                        tracks.track_id NOT IN (SELECT track_id FROM errors)
                        AND tracks.track_id = beats.track_id
                        AND tracks.crawl_start = beats.crawl_start
                        AND tracks.track_id = bars.track_id
                        AND tracks.crawl_start = bars.crawl_start
                        AND tracks.track_id = sections.track_id
                        AND tracks.crawl_start = sections.crawl_start
                        AND tracks.license_url IN
                        (
                            'http://creativecommons.org/licenses/by-sa/2.0/',
                            'http://creativecommons.org/licenses/by/2.0/'
                        )
                        AND tracks.crawl_start = :c
                    ORDER BY
                        beats.confidence DESC,
                        bars.confidence DESC,
                        sections.confidence DESC
                    LIMIT :x
                 )
            SELECT track_id
            FROM best
            ORDER BY random()
    ''')

    tids = [t[0] for t in conn.execute(s, c=crawl_start, x=limit)]

    if output:
        for tid in tids:
            log.info(tid)
    else:
        return tids

def lite(crawl_start, limit, output=True, *args, **kwargs):
    '''Return lite tracks from a particular crawl ranked by beats confidence.'''
    engine = make_engine()
    conn = engine.connect()
    s = text('''WITH beats AS (
                    SELECT track_id, crawl_start, avg(confidence) AS confidence
                    FROM beats
                    GROUP BY track_id, crawl_start
                    ORDER BY avg(confidence) DESC
                 ),
                 bars AS (
                    SELECT track_id, crawl_start, avg(confidence) AS confidence
                    FROM bars
                    GROUP BY track_id, crawl_start
                    ORDER BY avg(confidence) DESC
                 ),
                 sections AS (
                    SELECT track_id, crawl_start, avg(confidence) AS confidence
                    FROM sections
                    GROUP BY track_id, crawl_start
                    ORDER BY avg(confidence) DESC
                 ),
                 errors AS (
                    SELECT DISTINCT track_id
                    FROM sampler_errors
                 ),
                 best AS (
                    SELECT
                        tracks.track_id,
                        tracks.crawl_start,
                        tracks.license_url,
                        beats.confidence AS beats_confidence,
                        bars.confidence AS bars_confidence,
                        sections.confidence AS sections_confidence
                    FROM
                        tracks,
                        beats,
                        bars,
                        sections
                    WHERE
                        tracks.track_id NOT IN (SELECT track_id FROM errors)
                        AND tracks.track_id = beats.track_id
                        AND tracks.crawl_start = beats.crawl_start
                        AND tracks.track_id = bars.track_id
                        AND tracks.crawl_start = bars.crawl_start
                        AND tracks.track_id = sections.track_id
                        AND tracks.crawl_start = sections.crawl_start
                        AND tracks.license_url IN
                        (
                            'http://creativecommons.org/licenses/by-nc-sa/2.0/',
                            'http://creativecommons.org/licenses/by-nc/2.0/'
                        )
                        AND tracks.crawl_start = :c
                    ORDER BY
                        beats.confidence DESC,
                        bars.confidence DESC,
                        sections.confidence DESC
                    LIMIT :x
                 )
            SELECT track_id
            FROM best
            ORDER BY random()
    ''')

    tids = [t[0] for t in conn.execute(s, c=crawl_start, x=limit)]

    if output:
        for tid in tids:
            log.info(tid)
    else:
        return tids
