#!/usr/bin/env python

import os
import sys
import codecs
import re
import shutil

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

import salt.config


here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    # intentionally *not* adding an encoding option to open
    return codecs.open(os.path.join(here, *parts), 'r').read()

def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

readme = open('README.rst').read()
doclink = '''
Documentation
-------------

The full documentation is at http://epic.rtfd.org.'''
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

install_requires=[
    'boto',
    'SQLAlchemy',
    'psycopg2',
    'salt',
]
if os.environ.get('SAMPLER_INSTALL', None):
    src = os.path.join(here, 'epic', 'sampler', 'module.py')
    minion_opts = salt.config.minion_config(
            os.environ.get('SALT_MINION_CONFIG', '/etc/salt/minion'))
    dest = os.path.join(minion_opts['extension_modules'], 'modules',
                        'epicsampler.py')

    if not os.path.exists(os.path.dirname(dest)):
        os.makedirs(os.path.dirname(dest))

    shutil.copy(src, dest)
else:
    install_requires += [
        'Scrapy',
        'scrapylib',
        'pyechonest',
        'apache-libcloud',
    ]

class PyTest(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['--strict', '--verbose', '--tb=long', 'tests']
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)

setup(
    name='epic',
    version=find_version('epic', '__init__.py'),
    description='A tool to crawl, download, split, and package Creative Commons audio files from the web.',
    long_description=readme + '\n\n' + doclink + '\n\n' + history,
    author='A.J. Welch',
    author_email='awelch0100@gmail.com',
    url='https://github.com/ajw0100/epic',
    cmdclass={
        'test': PyTest,
    },
    entry_points={
        'console_scripts': [
            'epicdb = epic:EpicdbCmd.run',
            'epicbot = epic:EpicbotCmd.run',
            'epicsampler = epic:EpicsamplerCmd.run',
            'epicqry = epic:EpicqryCmd.run',
            'epicpkg = epic:EpicpkgCmd.run',
        ],
    },
    packages=find_packages(),
    package_dir={'epic': 'epic'},
    include_package_data=True,
    install_requires=install_requires,
    tests_require=['pytest'],
    test_suite='test.test_epic',
    extras_require={
        'testing': ['pytest'],
    },
    license='MIT',
    zip_safe=False,
    keywords='epic',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: Implementation :: PyPy',
    ]
)
