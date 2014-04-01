#!/usr/bin/env python

from setuptools import setup, find_packages


setup(
    name='epic.bot',
    version='0.1.0',
    description='Epic web crawler.',
    author='A.J. Welch',
    author_email='awelch0100@gmail.com',
    url='https://github.com/ajw0100/epic/bot',
    entry_points={
        'console_scripts': [
            'epicbot = epic.bot.cmd:EpicbotCmd.run',
        ]
    },
    namespace_packages = ['epic'],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'epic',
        'Scrapy',
        'scrapylib',
        'pyechonest',
        'boto',
        'SQLAlchemy',
        'psycopg2',
    ],
)
