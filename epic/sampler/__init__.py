# -*- coding: utf-8 -*-
'''
Distributes the sampling of tracks found by `epicbot` over multiple servers.
'''
import logging
import os
import datetime
from collections import OrderedDict as _OrderedDict
import curses
import json

import salt.config
import salt.cloud
import salt.output
import salt.utils.event
from salt.utils.event import tagify as _tagify


log = logging.getLogger(__name__)


MASTER_OPTS = salt.config.master_config(
    os.environ.get('SALT_MASTER_CONFIG', '/etc/salt/master'))

class _Cache(object):

    def __init__(self, name):
        dirname = os.path.join(MASTER_OPTS['cachedir'], 'epicsampler')
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        self.path = os.path.join(dirname, name)

    def read(self):
        '''
        Attempt to read from cache.
        '''
        try:
            return json.loads(open(self.path).read())
        except IOError:
            return []

    def write(self, data):
        '''
        Write data to cache.

        :param data: Data to write to cache.
        '''
        with open(self.path, 'w') as cache:
            cache.write(json.dumps(data))

    def purge(self):
        '''
        Remove cache file.
        '''
        try:
            os.remove(self.path)
        except OSError:
            pass


class _ActiveJobCache(_Cache):

    def __init__(self):
        super(_ActiveJobCache, self).__init__('active')

    def read(self):
        '''
        Attempt to read from cache.

        Purge cache and move jid to history if job is no longer active.
        '''
        contents = super(_ActiveJobCache, self).read()
        if not contents:
            return {}

        minions = _servers_up()
        local_client = _get_local_client()
        data = local_client.cmd(minions,
                                'saltutil.find_job',
                                arg=[contents['jid']],
                                expr_form='list',
                                timeout=MASTER_OPTS['timeout'])

        for server in data:
            if data[server]:
                # True. Cached jid is still active
                return contents

        # cached jid is no longer active on any servers
        # add cached jid to front of history list
        history_cache = _Cache('history')
        history_cache.write([contents['jid']] + history_cache.read())

        super(_ActiveJobCache, self).purge()
        return {}

    def jid(self):
        return self.read().get('jid', None)


def _get_local_client():
    return salt.client.LocalClient(mopts=MASTER_OPTS)

def _get_cloud_client():
    opts = salt.config.cloud_config(os.environ.get('SALT_CLOUD_CONFIG',
            os.path.join(os.path.dirname(MASTER_OPTS['conf_file']), 'cloud')))
    return salt.cloud.CloudClient(opts=opts)

def up(profile, servers=1, display_ssh_output=False, *args, **kwargs):
    '''
    Spin up servers in parallel.

    CLI Example::

    .. code-block:: bash

        salt-run -l info epicsampler.up profile=ec2_c3l_ubuntu servers=10
    '''
    server_cache = _Cache('server')
    if server_cache.read():
        log.info('Servers are already up. Run `epicsampler ping` to see '
            'status.')
        return

    log.info('Spinning up {0} servers. This may take a while'.format(servers))
    if not display_ssh_output:
        log.info('SSH output has been disabled. Set cli option '
             '--ssh_output=True to enable.')

    names = ['sampler-{0:02d}'.format(n) for n in xrange(servers)]
    cloud_client = _get_cloud_client()
    try:
        # using cloud_client with start_action='state.highstate' doesn't
        # succesfully complete with many servers. state.highstate should be run
        # manually for now.
        cloud_client.profile(profile=profile, names=names,
            parallel=True, display_ssh_output=display_ssh_output,
            script_args='git v2014.1.0', show_deploy_args=True)
    except salt.cloud.exceptions.SaltCloudConfigError, e:
        log.info(e)
        return

    server_cache.write(names)

    return names

def ping(output=True, *args, **kwargs):
    '''
    Ping servers and return up/down status.

    CLI Example::

    .. code-block:: bash

        salt-run -l info epicsampler.ping
    '''
    ret = {}
    cached_servers = _Cache('server').read()
    local_client = _get_local_client()

    if not cached_servers:
        ret['up'] = []
        ret['down'] = []
    else:
        minions = local_client.cmd(cached_servers,
                                   'test.ping',
                                   expr_form='list',
                                   timeout=MASTER_OPTS['timeout'])
        ret['up'] = sorted(minions)
        ret['down'] = sorted(set(cached_servers) - set(minions))

    if output:
        salt.output.display_output(ret, '', MASTER_OPTS)
    return ret

def _servers_down():
    '''
    Return a list of all sampler servers that are down or unresponsive.
    '''
    return ping(output=False).get('down', [])

def _servers_up():
    '''
    Return a list of all sampelrs servers that are up.
    '''
    return ping(output=False).get('up', [])

def provision(*args, **kwargs):
    '''
    Provision available servers
    '''
    local_client = _get_local_client()

    minions = _servers_up()
    if not minions:
        log.info('No servers have been spun up. Run `epicsampler up`')
        return

    log.info('Installing python2.')
    data = local_client.cmd(minions,
                            'state.single',
                            arg=[],
                            kwarg={
                                'fun': 'pkg.installed',
                                'name': 'python',
                            },
                            expr_form='list',
                            timeout=300)
    salt.output.display_output(data, '', MASTER_OPTS)

    log.info('Installing python-dev.')
    data = local_client.cmd(minions,
                            'state.single',
                            arg=[],
                            kwarg={
                                'fun': 'pkg.installed',
                                'name': 'python-dev',
                            },
                            expr_form='list',
                            timeout=300)
    salt.output.display_output(data, '', MASTER_OPTS)

    log.info('Installing libpq-dev.')
    data = local_client.cmd(minions,
                            'state.single',
                            arg=[],
                            kwarg={
                                'fun': 'pkg.installed',
                                'name': 'libpq-dev',
                            },
                            expr_form='list',
                            timeout=300)
    salt.output.display_output(data, '', MASTER_OPTS)

    log.info('Adding apt repo deb http://mp3splt.sourceforge.net/repository '
             'precise main.')
    data = local_client.cmd(minions,
                            'state.single',
                            arg=[],
                            kwarg={
                                'fun': 'pkgrepo.managed',
                                'name': 'deb http://mp3splt.sourceforge.net/repository precise main',
                            },
                            expr_form='list',
                            timeout=300)
    salt.output.display_output(data, '', MASTER_OPTS)

    log.info('Installing libmp3splt0-mp3, libmp3splt0-ogg, libmp3splt0-flac, '
             'mp3splt.')
    data = local_client.cmd(minions,
                            'state.single',
                            arg=[],
                            kwarg={
                                'fun': 'pkg.installed',
                                'name': None,
                                'pkgs': [
                                    'libmp3splt0-mp3',
                                    'libmp3splt0-ogg',
                                    'libmp3splt0-flac',
                                    'mp3splt',
                                ],
                                'skip_verify': True
                            },
                            expr_form='list',
                            timeout=300)
    salt.output.display_output(data, '', MASTER_OPTS)

    log.info('Downloading pip install script.')
    data = local_client.cmd(minions,
                            'state.single',
                            arg=[],
                            kwarg={
                                'fun': 'cmd.run',
                                'cwd': '/tmp',
                                'name': 'wget https://raw.github.com/pypa/pip/master/contrib/get-pip.py',
                            },
                            expr_form='list',
                            timeout=300)
    salt.output.display_output(data, '', MASTER_OPTS)

    log.info('Installing pip.')
    data = local_client.cmd(minions,
                            'state.single',
                            arg=[],
                            kwarg={
                                'fun': 'cmd.run',
                                'cwd': '/tmp',
                                'name': 'python get-pip.py',
                            },
                            expr_form='list',
                            timeout=300)
    salt.output.display_output(data, '', MASTER_OPTS)

    log.info('Cloning epic git repo.')
    data = local_client.cmd(minions,
                            'state.single',
                            arg=[],
                            kwarg={
                                'fun': 'git.latest',
                                'name': 'https://github.com/ajw0100/epic.git',
                                'target': '/tmp/epic',
                                'force': True,
                                'force_checkout': True,
                            },
                            expr_form='list',
                            timeout=300)
    salt.output.display_output(data, '', MASTER_OPTS)

    log.info('Installing epic requirements.')
    data = local_client.cmd(minions,
                            'state.single',
                            arg=[],
                            kwarg={
                                'fun': 'cmd.run',
                                'name': 'pip install -r ./epic/requirements_sampler.txt',
                                'cwd': '/tmp',
                            },
                            expr_form='list',
                            timeout=300)
    salt.output.display_output(data, '', MASTER_OPTS)

    log.info('Installing epic.')
    data = local_client.cmd(minions,
                            'state.single',
                            arg=[],
                            kwarg={
                                'fun': 'cmd.run',
                                'name': 'SAMPLER_INSTALL=true pip install ./epic',
                                'cwd': '/tmp',
                            },
                            expr_form='list',
                            timeout=300)
    salt.output.display_output(data, '', MASTER_OPTS)

def run(crawl_start, spider, offset=0, qty=-1, *args, **kwargs):
    '''
    Run sampler across all available servers.

    CLI Example::

    .. code-block:: bash

        salt-run -l info epicsampler.run crawl_start=2014-01-20T01-34-37 spider=soundclick qty=1000
    '''
    ret = {}
    active_cache = _ActiveJobCache()
    local_client = _get_local_client()

    log.info('Checking for active job.')
    if active_cache.jid():
        log.info('%s is already running. Run `epicsampler kill` to kill '
            'active job.', active_cache.jid())
        return

    log.info('Querying available servers.')
    minions = _servers_up()
    if not minions:
        log.info('No servers have been spun up. Run `epicsampler up`')
        return

    log.info('Running epicsampler.run across available servers.')
    sampler_start = '{:%Y-%m-%dT%H-%M-%S}'.format(datetime.datetime.now())
    envars = {
        'AWS_ACCESS_KEY_ID': os.environ.get('AWS_ACCESS_KEY_ID', None),
        'AWS_SECRET_ACCESS_KEY': os.environ.get('AWS_SECRET_ACCESS_KEY', None),
        'EPIC_S3_BUCKET': os.environ.get('EPIC_S3_BUCKET', None),
    }
    data = local_client.run_job(minions,
                                'epicsampler.run',
                                arg=[],
                                kwarg={
                                    'crawl_start': crawl_start,
                                    'spider': spider,
                                    'sampler_start': sampler_start,
                                    'minions': len(minions),
                                    'offset': offset,
                                    'qty': qty,
                                    'envars': envars,
                                },
                                expr_form='list',
                                timeout=MASTER_OPTS['timeout'])
    ret['jid'] = data['jid']
    ret['_stamp'] = sampler_start
    ret['results'] = _OrderedDict({m: {} for m in sorted(minions)})
    active_cache.write(ret)

    salt.output.display_output(ret, '', MASTER_OPTS)
    return ret

def _render_help(stdscr):
    stdscr.nodelay(0)
    stdscr.clear()
    stdscr.addstr(0, 0, '{:<40s}'.format('HELP'), curses.A_REVERSE)
    stdscr.addstr(0, 40, '{:>37s}'.format('Press any key to return.'),
        curses.A_REVERSE)

    lines = [
        ('SERVER ID',  'ID of server reporting stats.'),
        ('RUNTIME',    'Updated when new events are sent from server.'),
        ('ASSIGNED',   '# of tracks server was assigned to process.'),
        ('DOWNLOADED', '# of tracks server has downloaded from src bucket.'),
        ('PROCESSED',  '# of tracks server has finished processing.'),
        ('SECTIONS',   '# of sections processsd.'),
        ('BARS',       '# of bars processed.'),
        ('BEATS',      '# of beats processed.'),
        ('E',          '# of errors encountered.'),
        ('C',          'Completed flag.'),
    ]
    for i, line in enumerate(lines):
        stdscr.addstr(i+1, 0,
            '{0:<20s}{1:7s}{2:<50s}'.format(line[0], ' ', line[1]))
    stdscr.refresh()
    if stdscr.getch():
        stdscr.nodelay(1)
        stdscr.clear()

def _render_detail(stdscr, jid, data):
    header = [
        [
            ('<', 27, 'JOB ID: {0}'.format(jid)),
            ('>', 50, 'Press h for help and any other key to return.'),
        ],
        [
            ('<', 11, 'SERVER ID'),
            ('>', 8,  'RUNTIME'),
            ('>', 9,  'ASSIGNED'),
            ('>', 11, 'DOWNLOADED'),
            ('>', 10, 'PROCESSED'),
            ('>', 9,  'SECTIONS'),
            ('>', 7,  'BARS'),
            ('>', 8,  'BEATS'),
            ('>', 2,  'E'),
            ('>', 2,  'C'),
        ],
    ]
    for y, line in enumerate(header):
        x = 0
        for span in line:
            stdscr.addstr(y, x, '{2:{0}{1:d}s}'.format(*span),
                          curses.A_REVERSE)
            x += span[1]

    lines = [
        (9,  'assigned_tracks'),
        (11, 'downloaded_tracks'),
        (10, 'processed_tracks'),
        (9,  'sections'),
        (7,  'bars'),
        (8,  'beats'),
        (2,  'errors'),
        (2,  'complete'),
    ]

    # render minion data and keep a running total
    total = {}
    for i, minion in enumerate(sorted(data)):
        y = i+2
        stdscr.addstr(y, 0, '{:<11s}'.format(minion))

        # handle runtime
        try:
            runtime = data[minion]['runtime'].split('.')[0]
        except KeyError:
            runtime = 'Updating'
        else:
            # set total['runtime'] to greatest runtime of all minions
            if 'runtime' not in total:
                total['runtime'] = runtime
            else:
                minion_split = runtime.split(':')
                minion_time = datetime.timedelta(hours=int(minion_split[0]),
                                               minutes=int(minion_split[1]),
                                               seconds=int(minion_split[2]))
                total_split = total['runtime'].split(':')
                total_time = datetime.timedelta(hours=int(total_split[0]),
                                               minutes=int(total_split[1]),
                                               seconds=int(total_split[2]))
                if minion_time > total_time:
                    total['runtime'] = runtime

        # render minion data
        stdscr.addstr(y, 11, '{:>8s}'.format(runtime))
        x = 19
        for line in lines:
            stdscr.addstr(y, x,
                '{1:{0}d}'.format(line[0], data[minion].get(line[1], 0)))
            try:
                total[line[1]] += data[minion].get(line[1], 0)
            except KeyError:
                total[line[1]] = data[minion].get(line[1], 0)
            x += line[0]

    # render totals
    y = len(data)+2
    stdscr.addstr(y, 0, '{:<11s}'.format('TOTAL'), curses.A_REVERSE)
    stdscr.addstr(y, 11, '{:>8s}'.format(total.get('runtime', 'Updating')),
        curses.A_REVERSE)
    x = 19
    for line in lines:
        # if all minions are complete, set complete total to 1
        # else set it to 0
        if line[1] == 'complete':
            if total[line[1]] == len(data):
                total_str = '{1:{0}d}'.format(line[0], 1)
            else:
                total_str = '{1:{0}d}'.format(line[0], 0)
        else:
            total_str = '{1:{0}d}'.format(line[0], total[line[1]])
        stdscr.addstr(y, x, total_str, curses.A_REVERSE)
        x += line[0]

    stdscr.refresh()

def _render_active_detail(stdscr, jid):
    stdscr.clear()
    active_cache = _ActiveJobCache()
    local_client = _get_local_client()

    # get cached results from epicsampler active job cache
    data = active_cache.read()
    sstamp = datetime.datetime.strptime(data['_stamp'], '%Y-%m-%dT%H-%M-%S')

    # Update data with job results from samplers that have already finished
    # and therefore will not fire events below.
    for minion, result in local_client.get_full_returns(jid, [], 0).items():
        ustamp = datetime.datetime.strptime(result['ret'].pop('_stamp'),
                                            '%Y-%m-%d_%H:%M:%S.%f')
        result['ret']['runtime'] = str(ustamp - sstamp)
        data['results'][minion] = result['ret']

    _render_detail(stdscr, jid, data=data['results'])

    # listen for events from sampler servers and refresh detail screen
    event = salt.utils.event.MasterEvent(MASTER_OPTS['sock_dir'])
    tag = _tagify(['monitor','update'], base='epicsampler')
    stdscr.nodelay(1)
    while True:
        evt = event.get_event(wait=0.5, tag=tag)
        if evt:
            ustamp = datetime.datetime.strptime(evt['_stamp'],
                                                '%Y-%m-%d_%H:%M:%S.%f')
            evt['data']['runtime'] = str(ustamp - sstamp)
            data['results'][evt['id']].update(evt['data'])
            _render_detail(stdscr, jid, data=data['results'])

        c = stdscr.getch()
        if c == ord('h'.encode('utf-8')):
            _render_help(stdscr)
            # render detail page right away when we return from help
            stdscr.clear()
            _render_detail(stdscr, jid, data=data['results'])
        elif c > 0:
            stdscr.nodelay(0)
            break
        else:
            continue
    active_cache.write(data)

def _render_historical_detail(stdscr, jid):
    stdscr.clear()
    local_client = _get_local_client()

    data = {
        'jid': jid,
    }

    # get job start timestamp
    # taken from https://github.com/saltstack/salt/blob/c8b96b901c608a6207f1fcd8bc582c3b5df519c6/salt/runners/jobs.py
    serial = salt.payload.Serial(MASTER_OPTS)
    jid_dir = salt.utils.jid_dir(jid, MASTER_OPTS['cachedir'],
                                 MASTER_OPTS['hash_type'])
    load_path = os.path.join(jid_dir, '.load.p')
    load = serial.load(salt.utils.fopen(load_path, 'rb'))
    sstamp = datetime.datetime.strptime(load['arg'][0]['sampler_start'],
                                        '%Y-%m-%dT%H-%M-%S')

    # get job results from job cache and calc runtime
    returns = local_client.get_full_returns(jid, [], 0)
    data['results'] = _OrderedDict({m: {} for m in sorted(returns.keys())})
    for minion, result in returns.items():
        ustamp = datetime.datetime.strptime(result['ret'].pop('_stamp'),
                                            '%Y-%m-%d_%H:%M:%S.%f')
        result['ret']['runtime'] = str(ustamp - sstamp)
        data['results'][minion] = result['ret']

    _render_detail(stdscr, jid, data=data['results'])

    while True:
        c = stdscr.getch()
        if c == ord('h'.encode('utf-8')):
            _render_help(stdscr)
            # render detail page right away when we return from help
            stdscr.clear()
            _render_detail(stdscr, jid, data=data['results'])
        elif c > 0:
            break
        else:
            continue

def _render_menu(stdscr):
    # turn off blinking cursor
    curses.curs_set(0)

    active_cache = _ActiveJobCache()
    history_cache = _Cache('history')

    active = [active_cache.jid()]
    history = history_cache.read()
    jids = [jid for jid in active + history if jid is not None]

    option = 0
    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, '{:^77s}'.format('MENU'), curses.A_REVERSE)
        stdscr.addstr(1, 0, '{:^77s}'.format('Up/down arrow keys to navigate.'
                                             ' Enter to select. Any other key '
                                             'to exit.'),
                      curses.A_REVERSE)

        if not jids:
            stdscr.addstr(2, 0, '{:^77s}'.format('No jobs have been run.'))
            stdscr.refresh()
            c = stdscr.getch()
            if c > 0:
                break
            else:
                continue
        else:
            highlight = [0]*len(jids)
            highlight[option] = curses.A_REVERSE
            for i, jid in enumerate(jids):
                stdscr.addstr(i+3, 0, '{:^77s}'.format(jid), highlight[i])
            stdscr.refresh()
            c = stdscr.getch()
            if c == curses.KEY_UP:
                option = (option-1)%len(jids)
            elif c == curses.KEY_DOWN:
                option = (option+1)%len(jids)
            elif c == ord('\n'.encode('utf-8')):
                if jids[option] == active_cache.jid():
                    _render_active_detail(stdscr, jids[option])
                else:
                    _render_historical_detail(stdscr, jids[option])
            elif c > 0:
                break
            else:
                continue

def monitor(*args, **kwargs):
    '''
    Monitor progress of active sampler job. View results of historical jobs.

    CLI Example::

    .. code-block:: bash

        salt-run -l info epicsampler.monitor
    '''
    curses.wrapper(_render_menu)

def kill(*args, **kwargs):
    '''
    Kill active sampler job.

    CLI Example::

    .. code-block:: bash

        salt-run -l info epicsampler.kill
    '''
    active_cache = _ActiveJobCache()

    if not active_cache.jid():
        log.info('No active sampler job.')
        return

    minions = _servers_up()
    local_client = _get_local_client()
    ret = local_client.cmd(minions,
                            'saltutil.kill_job',
                            arg=[active_cache.jid()],
                            expr_form='list',
                            timeout=MASTER_OPTS['timeout'])

    active_cache.purge()
    salt.output.display_output(ret, '', MASTER_OPTS)
    return ret

def destroy(*args, **kwargs):
    '''
    Destroy servers.

    CLI Example::

    .. code-block:: bash

        salt-run -l info epicsampler.destroy
    '''
    ret = {}
    server_cache = _Cache('server')

    cached_servers = server_cache.read()
    if not cached_servers:
        log.info('No servers to destroy.')
        return

    minions = _servers_up()
    cloud_client = _get_cloud_client()
    try:
        ret = cloud_client.destroy(minions)
    except salt.cloud.exceptions.SaltCloudSystemExit, e:
        log.info(e)

    server_cache.purge()
    salt.output.display_output(ret, '', MASTER_OPTS)
    return ret
