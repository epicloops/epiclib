#!/usr/bin/env python

from setuptools import setup, find_packages


setup(
    name='epic.sampler',
    version='0.1.0',
    description='Epic mp3 sampler.',
    author='A.J. Welch',
    author_email='awelch0100@gmail.com',
    url='https://github.com/ajw0100/epic/sampler',
    entry_points={
        'console_scripts': [
            'epicsampler = epic.sampler.cmd:EpicsamplerCmd.run',
        ]
    },
    namespace_packages = ['epic'],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'epic',
        'boto',
        'SQLAlchemy',
        'psycopg2',
    ],
)
