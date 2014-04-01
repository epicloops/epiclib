#!/usr/bin/env python

from setuptools import setup, find_packages


setup(
    name='epic',
    version='0.1.0',
    description='Base epic package.',
    author='A.J. Welch',
    author_email='awelch0100@gmail.com',
    url='https://github.com/ajw0100/epic/epic',
    entry_points={
        'console_scripts': [
            'epicdb = epic.db.cmd:EpicdbCmd.run',
        ]
    },
    namespace_packages = ['epic'],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'boto',
        'SQLAlchemy',
        'psycopg2',
    ],
)
