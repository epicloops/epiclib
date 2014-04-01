# epic
- [Overview](#overview)
- [Structure](#structure)
- [Installation](#installation)
- [Config](#config)
- [Usage](#usage)
- [TODO](#todo)

<a name="overview"/>
## Overview
This repo contains the distributed web crawler and mp3 splitter that powers
[epicloops.com](http://epicloops.com/). The goal of
[epicloops.com](http://epicloops.com/) is to use Creative Commons audio files
from the web as a source of loops and samples to be integrated into
projects built with [GarageBand](https://www.apple.com/mac/garageband/),
[Logic](https://www.apple.com/logic-pro/),
[ProTools](http://www.avid.com/us/products/family/pro-tools/), etc.

<a name="structure"/>
## Structure
The structure of this repo is a little unorthodox because I am using
setuptools' [namespace packages](http://pythonhosted.org/setuptools/setuptools.html#namespace-packages)
to separate the installation of each component. See the Installation section
for more info. Essentially, the [epic/](epic/), [epic.bot/](epic.bot/),
[epic.sampler/](epic.sampler/) directories could be split into their own
repositories.

### [epic/](epic/)
This is the base epic package. This includes the database models as well as a
script to create, truncate and drop the database schema. It also includes
utility functions and classes to interact with s3, sqs, and the local
filesystem. Both [epic.bot/](epic.bot/) and [epic.sampler/](epic.sampler/)
require this package to be installed.

### [epic.bot/](epic.bot/)
This package contains a [scrapy](https://github.com/scrapy/scrapy) project
that crawls specific sites looking for Creative Commons audio files. The sites
it is currently capable of crawling include:

- [soundclick.com](http://www.soundclick.com/)
- more to come...

The scrapy [pipeline](http://doc.scrapy.org/en/latest/topics/item-pipeline.html)
is used to ensure the file has a CC license, download the file and store it
on s3, gather data about the file from the [echonest api](http://the.echonest.com/),
persist this data to a database, and notify the samplers through sqs that the
file is ready to be split.

### [epic.sampler/](epic.sampler/)
This package is responsible for splitting audio files found by [epic.bot/](epic.bot/)
into sections, bars and beats. It first listens for messages from sqs
indicating a file is ready to be split. Then it gets the file from s3, queries
the database to get the echonest data related to that file and uses this data to
split the file with
[libmp3splt](http://mp3splt.sourceforge.net/mp3splt_page/home.php).

<a name="installation"/>
## Installation
The `epic` package is a [namespace package](http://pythonhosted.org/setuptools/setuptools.html#namespace-packages)
which allows the `epic.bot` and `epic.sampler` packages to be installed
independently of each other. This is desirable for two reasons:

- `epic.bot` is a web crawler and therefore memory and network intensive.
`epic.sampler` is an mp3 splitter and therefore cpu intensive. Ideally these
will be run on separate boxes with specs that suit their individual needs.
- `epic.bot` has dependencies that `epic.sampler` does not require and vice
versa. As separate packages, we only have to install the dependencies that are
absolutely required for a particular component.

### Installation steps:
1. Clone the repo:
```
git clone https://github.com/ajw0100/epic.git
```
2. Install `epic`:
```
# epic
# ----
# Make sure sqlalchemy drivers are installed

pip install -r ./epic/epic/requirements.txt ./epic/epic
```
3. Install `epic.bot` and/or `epic.sampler`:
```
# epic.bot
# --------
# Make sure scrapy dependencies are installed

pip install -r ./epic/epic.bot/requirements.txt ./epic/epic.bot


# epic.sampler
# ------------
# Make sure libmp3splt is installed

pip install -r ./epic/epic.sampler/requirements.txt ./epic/epic.sampler
```

### Installation example:
For a rough working example of how to get this up and running see this saltstack
repo: [https://github.com/ajw0100/epic-states](https://github.com/ajw0100/epic-states)

<a name="config"/>
## Config
A json config file must be placed at `~/.epic/config`. Here is an example:
```
{
    "SQLALCHEMY_DATABASE_URI": "sqlite:////tmp/my_database.db",
    "AWS_ACCESS_KEY_ID": "XXXXXXXXXXXXXXXXXXXX",
    "AWS_SECRET_ACCESS_KEY": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "AWS_REGION": "us-east-1",
    "AWS_S3_BUCKET": "epic",
    "CRAWLERA_USER": "user",
    "CRAWLERA_PASS": "pass",
    "ECHONEST_API_KEY": "XXXXXXXXXXXXXXXXX"
}
```
**Note:** [crawlera](http://crawlera.com/) and [echonest](http://echonest.com/)
accounts are required and the aws credentials must have full access to the s3
bucket and sqs.

<a name="usage"/>
## Usage
If everything is installed and configured, the following commands are
available:

### `epicdb`
```
➜ epicdb create
[INFO    ] Schema created.
➜ epicdb truncate
[INFO    ] section truncated.
[INFO    ] segment truncated.
[INFO    ] processingerror truncated.
[INFO    ] droppedtrack truncated.
[INFO    ] sample truncated.
[INFO    ] track truncated.
➜ epicdb drop
[INFO    ] Schema dropped.
➜
```

### `epicbot`
```
➜  epicbot crawl soundclick
2014-04-01 00:14:30+0000 [scrapy] INFO: Scrapy 0.22.2 started (bot: epicbot)
2014-04-01 00:14:30+0000 [scrapy] INFO: Optional features available: ssl, http11, boto
2014-04-01 00:14:30+0000 [scrapy] INFO: Overridden settings: {'CLOSESPIDER_ITEMCOUNT': 1000, 'CLOSESPIDER_ERRORCOUNT': 20, 'SPIDER_MODULES': ['epic.bot.spiders'], 'BOT_NAME': 'epicbot', 'CLOSESPIDER_PAGECOUNT': 20000, 'DOWNLOAD_DELAY': 5}
2014-04-01 00:14:30+0000 [scrapy] INFO: Enabled extensions: AutoThrottle, LogStats, TelnetConsole, CloseSpider, WebService, CoreStats, SpiderState, ExtStats, PersistDroppedItems
2014-04-01 00:14:30+0000 [scrapy] INFO: Enabled downloader middlewares: HttpAuthMiddleware, DownloadTimeoutMiddleware, UserAgentMiddleware, RetryMiddleware, DefaultHeadersMiddleware, MetaRefreshMiddleware, HttpCompressionMiddleware, RedirectMiddleware, CrawleraMiddleware, CookiesMiddleware, ChunkedTransferMiddleware, DownloaderStats
2014-04-01 00:14:30+0000 [scrapy] INFO: Enabled spider middlewares: HttpErrorMiddleware, OffsiteMiddleware, RefererMiddleware, UrlLengthMiddleware, DepthMiddleware
2014-04-01 00:14:30+0000 [scrapy] INFO: Enabled item pipelines: PostCrawlPipeline, DuplicatesPipeline, CCFilterPipeline, TrackPipeline, EchonestPipeline, DbPipeline, QueuePipeline
2014-04-01 00:14:30+0000 [soundclick] INFO: Spider opened
2014-04-01 00:14:30+0000 [soundclick] INFO: Crawled 0 pages (at 0 pages/min), scraped 0 items (at 0 items/min)
2014-04-01 00:14:30+0000 [soundclick] INFO: Using crawlera at http://proxy.crawlera.com:8010 (user: user)
2014-04-01 00:14:30+0000 [scrapy] DEBUG: Telnet console listening on 0.0.0.0:6023
2014-04-01 00:14:30+0000 [scrapy] DEBUG: Web service listening on 0.0.0.0:6080
2014-04-01 00:14:31+0000 [soundclick] DEBUG: Crawled (200) <GET http://www.soundclick.com/business/license_list.cfm?cclicense=1&sort=1&page=1&genreID=1> (referer: None)
2014-04-01 00:14:34+0000 [soundclick] DEBUG: Crawled (200) <GET http://www.soundclick.com/business/license_list.cfm?cclicense=1&sort=1&page=1&genreID=16> (referer: None)
2014-04-01 00:14:35+0000 [soundclick] DEBUG: Crawled (200) <GET http://www.soundclick.com/business/license_list.cfm?cclicense=1&sort=1&page=1&genreID=12> (referer: None)
2014-04-01 00:14:35+0000 [soundclick] DEBUG: Crawled (200) <GET http://www.soundclick.com/business/license_list.cfm?cclicense=1&sort=1&page=1&genreID=13> (referer: None)
2014-04-01 00:14:35+0000 [soundclick] DEBUG: Crawled (200) <GET http://www.soundclick.com/business/license_list.cfm?cclicense=1&sort=1&page=1&genreID=17> (referer: None)
2014-04-01 00:14:35+0000 [soundclick] DEBUG: Crawled (200) <GET http://www.soundclick.com/business/license_list.cfm?cclicense=1&sort=1&page=1&genreID=2> (referer: None)
2014-04-01 00:14:37+0000 [soundclick] DEBUG: Crawled (200) <GET http://www.soundclick.com/business/license_list.cfm?cclicense=1&sort=1&page=1&genreID=9> (referer: None)
2014-04-01 00:14:37+0000 [soundclick] DEBUG: Crawled (200) <GET http://www.soundclick.com/business/license_list.cfm?cclicense=1&sort=1&page=1&genreID=15> (referer: None)
2014-04-01 00:14:38+0000 [soundclick] DEBUG: Redirecting (302) to <GET http://www.soundclick.com/bands/default.cfm?bandID=233058> from <GET http://www.soundclick.com/michaelborkson>
2014-04-01 00:14:38+0000 [soundclick] DEBUG: Crawled (200) <GET http://www.soundclick.com/business/license_list.cfm?cclicense=1&sort=1&page=1&genreID=5> (referer: None)
2014-04-01 00:14:39+0000 [soundclick] DEBUG: Crawled (200) <GET http://www.soundclick.com/business/license_list.cfm?cclicense=1&sort=1&page=1&genreID=3> (referer: None)
2014-04-01 00:14:39+0000 [soundclick] DEBUG: Crawled (200) <GET http://www.soundclick.com/business/license_list.cfm?cclicense=1&sort=1&page=1&genreID=210> (referer: None)
2014-04-01 00:14:39+0000 [soundclick] DEBUG: Redirecting (302) to <GET http://www.soundclick.com/bands/default.cfm?bandID=1336797> from <GET http://www.soundclick.com/JakeRyan>
2014-04-01 00:14:40+0000 [soundclick] DEBUG: Crawled (200) <GET http://www.soundclick.com/business/license_list.cfm?cclicense=1&sort=1&page=1&genreID=10> (referer: None)
2014-04-01 00:14:43+0000 [soundclick] DEBUG: Crawled (200) <GET http://www.soundclick.com/business/license_list.cfm?cclicense=1&sort=1&page=2&genreID=1> (referer: http://www.soundclick.com/business/license_list.cfm?cclicense=1&sort=1&page=1&genreID=1)
2014-04-01 00:14:43+0000 [soundclick] DEBUG: Redirecting (302) to <GET http://www.soundclick.com/bands/default.cfm?bandID=404894> from <GET http://www.soundclick.com/26andbandless>
2014-04-01 00:14:43+0000 [soundclick] DEBUG: Redirecting (302) to <GET http://www.soundclick.com/bands/default.cfm?bandID=1026697> from <GET http://www.soundclick.com/alfonsobaro>
2014-04-01 00:14:44+0000 [soundclick] DEBUG: Crawled (200) <GET http://www.soundclick.com/business/license_list.cfm?cclicense=1&sort=1&page=2&genreID=16> (referer: http://www.soundclick.com/business/license_list.cfm?cclicense=1&sort=1&page=1&genreID=16)
```

### `epicsampler`
```
➜  epicsampler
[INFO    ] Queue empty. Checking again in 15 seconds.
[INFO    ] Queue empty. Checking again in 15 seconds.
[INFO    ] Queue empty. Checking again in 15 seconds.
[INFO    ] Processing 3f1844916e53ea24ccd839343ca4018b
[INFO    ] Removed /home/ubuntu/.epic/tmp
[INFO    ] Got s3 key: 2014-04-01T00:18:15.968766/3f1844916e53ea24ccd839343ca4018b/track.mp3 to /home/ubuntu/.epic/tmp/track.mp3
[INFO    ] Created /home/ubuntu/.epic/tmp/bar
[INFO    ] Wrote to /home/ubuntu/.epic/tmp/bar.cue
[INFO    ] Created /home/ubuntu/.epic/tmp/beat
[INFO    ] Wrote to /home/ubuntu/.epic/tmp/beat.cue
[INFO    ] Created /home/ubuntu/.epic/tmp/section
[INFO    ] Wrote to /home/ubuntu/.epic/tmp/section.cue
mp3splt 2.6 (20/07/13) - using libmp3splt 0.9.0
    Matteo Trotta <mtrotta AT users.sourceforge.net>
    Alexandru Munteanu <m AT ioalex.net>
THIS SOFTWARE COMES WITH ABSOLUTELY NO WARRANTY! USE AT YOUR OWN RISK!
[INFO    ] Set s3 key: 2014-04-01T00:18:15.968766/3f1844916e53ea24ccd839343ca4018b/bars/0001.mp3
[INFO    ] Set s3 key: 2014-04-01T00:18:15.968766/3f1844916e53ea24ccd839343ca4018b/bars/0002.mp3
[INFO    ] Set s3 key: 2014-04-01T00:18:15.968766/3f1844916e53ea24ccd839343ca4018b/bars/0003.mp3
[INFO    ] Set s3 key: 2014-04-01T00:18:15.968766/3f1844916e53ea24ccd839343ca4018b/bars/0004.mp3
[INFO    ] Set s3 key: 2014-04-01T00:18:15.968766/3f1844916e53ea24ccd839343ca4018b/bars/0005.mp3
[INFO    ] Set s3 key: 2014-04-01T00:18:15.968766/3f1844916e53ea24ccd839343ca4018b/bars/0006.mp3
```

<a name="todo"/>
TODO
----
- Clean up and unify logging.
- Clean up config file parsing.
- Tests!!
- Docs!!
- Potentially use twisted for s3 calls in sampler.
- Potentially make sampler multi-process.
- Potentially create python bindings for libmp3splt to avoid subprocess call
- `epic.app`: Monitoring and packaging webapp.
