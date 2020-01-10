#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='emoji-data',

    packages=find_packages('src'),
    package_dir={'': 'src'},

    description='A library represents emoji sequences and characters in Unicode® Technical Standard #51 Data Files',
    url='https://github.com/tanbro/emoji-data',
    author='liu xue yan',
    author_email='liu_xue_yan@foxmail.com',
    license='AGPLv3+',
    keywords='emoji unicode',

    use_scm_version={
        # guess-next-dev:	automatically guesses the next development version (default)
        # post-release:	generates post release versions (adds postN)
        'version_scheme': 'guess-next-dev',
        'write_to': 'src/emoji_data/version.py',
    },
    setup_requires=[
        'setuptools_scm',
        'setuptools_scm_git_archive',
    ],
    install_requires=[],

    python_requires='>=3.5',

    package_data={
        '': ['data/*']
    },

    classifiers=[
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Topic :: Text Processing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)
