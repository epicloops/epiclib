# -*- coding: utf-8 -*-
'''
Soundclick.com spider.
'''
from __future__ import unicode_literals

import re

from scrapy.spider import Spider
from scrapy.http import Request
from scrapy.selector import Selector

from epic.bot.options import Options
from epic.bot.utils import errback
from epic.bot.spiders.soundclick import settings
from epic.bot.spiders.soundclick.items import SoundclickTrackItem
from epic.bot.spiders.soundclick.loaders import SoundclickTrackItemLoader


class SoundclickSpider(Spider):

    name = 'soundclick'
    loader = SoundclickTrackItemLoader

    def __init__(self, max_tracks=None, start_page=1, max_pages=None,
                 genre='prod', *args, **kwargs):

        self.opts = Options(max_tracks, start_page, max_pages)

        self.base_url = 'http://www.soundclick.com'
        self.search_url = '{}/business/license_list.cfm'.format(self.base_url)

        self._start_urls = None
        self.start_urls = genre

        super(SoundclickSpider, self).__init__(*args, **kwargs)

    @property
    def start_urls(self):
        return self._start_urls

    @start_urls.setter
    def start_urls(self, value):

        page = self.opts.start_page
        base = '{}?cclicense=1&sort=1&page={}'.format(self.search_url, page)
        genre_map = settings.GENRE_MAP.items()
        genre_urls = {k: '{}&genreID={}'.format(base, v) for k, v in genre_map}
        options = {
            'all': genre_urls.values(),
            'prod': [
                genre_urls['acoustic'],
                genre_urls['alt'],
                genre_urls['blues'],
                genre_urls['classical'],
                genre_urls['comedy'],
                genre_urls['country'],
                genre_urls['electronic'],
                genre_urls['jazz'],
                genre_urls['latin'],
                genre_urls['metal'],
                genre_urls['pop'],
                genre_urls['rock'],
                genre_urls['poetry'],
                genre_urls['world'],
            ],
        }
        options.update({k: [v] for k, v in genre_urls.items()})

        if value.lower() not in options.keys():
            raise ValueError('Unknown genre')

        self._start_urls = options[value.lower()]

    def next_search_page_request(self, page, genre_id):
        # Generates next search page url. Soundclick stops listing
        # pages in their pagination after 10 so we must enumerate the
        # pages instead of crawling using a CrawlSpider Rule().
        qry = '?cclicense=1&sort=1&page={}&genreID={}'.format(page+1, genre_id)
        return Request(''.join([self.search_url, qry]), callback=self.parse)

    def parse(self, response):

        # Page-level data
        # ===============
        page = int(re.search(r'&page=(\d+)', response.url).group(1))

        sel = Selector(response)
        genre = sel.xpath('/html/body/table[1]/tr/td/div[2]/form/select[2]/'
                          'option[@selected="selected"]/text()').extract()
        genre_id = int(re.search(r'&genreID=(\d+)', response.url).group(1))

        # Track-level data
        # ================
        # First track is on row 4. Next track is 6 rows below.
        # Assuming 100 tracks per page, the xpath for the final row is:
        # /html/body/table[2]/tbody/tr[598]
        for i in xrange(4, 599, 6):

            # Return next search page if we are greater than max_tracks
            if self.opts.max_tracks and i == (4+(self.opts.max_tracks*6)):
                break

            loader = self.loader(item=SoundclickTrackItem(), response=response)

            # Each track's data is split across 2 rows in the tracks table
            trow1 = '/html/body/table[2]/tr[{}]'.format(i)
            trow2 = '/html/body/table[2]/tr[{}]'.format(i+2)

            # Ensure we have a track
            if not loader.get_xpath(trow1):

                # Attempt to crawl at least 100 pages per genre
                # TODO: Better way to recover from bad http responses?
                if self.opts.start_page and (self.opts.start_page+page) < 100:
                    break
                else:
                    return

            loader.add_value('origin_page_url', response.url)
            loader.add_value('genre', genre)
            loader.add_xpath('soundclick_songid',
                             '{}/td[1]/a[2]/@href'.format(trow1),
                             re=r'songid=(\d+)&')
            loader.add_xpath('artist', '{}/td[3]/a/text()'.format(trow1))
            loader.add_xpath('artist_page_url', '{}/td[3]/a/@href'.format(
                                                                        trow1))
            loader.add_xpath('title', '{}/td[4]/text()'.format(trow1))
            loader.add_xpath('soundclick_commercial',
                             '{}/td[5]/text()'.format(trow1))
            loader.add_xpath('soundclick_modifications',
                             '{}/td[6]/text()'.format(trow1))
            loader.add_xpath('license_url', '{}/td[8]/a/@href'.format(trow1))
            loader.add_xpath('sub_genre', '{}/td[2]/span/text()'.format(trow2))
            loader.add_xpath('description', '{}/td[2]/text()'.format(trow2))

            item = loader.load_item()

            yield Request(item['artist_page_url'],
                          callback=self.parse_artist_page,
                          errback=lambda f, i=item: errback(f, i),
                          # TODO: Cache parse_artist_page result to avoid this?
                          # Dont filter dup requests to artist page in case of
                          # multiple tracks per artist.
                          dont_filter=True,
                          meta={'item': item})

        # do not crawl more than max_pages
        if (self.opts.max_pages and
           ((page+1)-self.opts.start_page) == self.opts.max_pages):
            return
        else:
            yield self.next_search_page_request(page, genre_id)

    def parse_artist_page(self, response):

        loader = self.loader(item=response.meta['item'], response=response)
        match = re.search(r'bandID=(\d+)', response.url.decode('ascii'))
        if match:
            loader.add_value('soundclick_artist_id', match.group(1))
        item = loader.load_item()

        url = ''.join([self.base_url,
                       '/bands/page_songInfo.cfm',
                       '?songID={item[soundclick_songid]}'.format(item=item),
                       '&bandID='
                       '{item[soundclick_artist_id]}'.format(item=item),])

        return Request(url, callback=self.parse_track_page,
                       errback=lambda f, i=item: errback(f, i),
                       meta={'item': item})

    def parse_track_page(self, response):

        loader = self.loader(item=response.meta['item'], response=response)
        loader.add_value('track_page_url', response.url)
        loader.add_xpath('soundclick_download_url',
                         '//html',
                         re=r'/util/downloadSong\.cfm\?ID=' +
                            loader.item['soundclick_songid'])
        if loader.get_output_value('soundclick_download_url'):
            loader.add_value('download_flag', 'Y')
        else:
            loader.add_value('download_flag', 'N')
        item = loader.load_item()

        url = ''.join([self.base_url,
                       '/util/xmlsong.cfm',
                       '?songid={item[soundclick_songid]}'.format(item=item),
                       '&q=hi'])

        return Request(url, callback=self.parse_xml_page,
                       errback=lambda f, i=item: errback(f, i),
                       meta={'item': item})

    def parse_xml_page(self, response):

        loader = self.loader(item=response.meta['item'], response=response)
        loader.add_value('soundclick_xml_url', response.url)
        loader.add_xpath('track_url', '//cdnFilename/text()')
        return loader.load_item()
