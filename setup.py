#!/usr/bin/env python
import os
import codecs
import re

from setuptools import setup, find_packages


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

readme = open('README.md').read()

setup(
    name='epiclib',
    version=find_version('epiclib', '__init__.py'),
    description='A library of common code for use with epic components.',
    long_description=readme,
    author='A.J. Welch',
    author_email='awelch0100@gmail.com',
    url='https://github.com/epicloops/epiclib',
    entry_points={
        'console_scripts': [
            'epicdb = epiclib.db.cmd:EpicdbCmd.run',
        ]
    },
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'boto',
        'SQLAlchemy',
        'psycopg2',
    ],
)
