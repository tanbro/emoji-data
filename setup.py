#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
setuptools script file
"""

from setuptools import setup, find_packages

setup(
    name='emoji-data',

    packages=find_packages('src'),
    package_dir={'': 'src'},

    description='emoji-data from Unicode® Emoji',
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
        'pytest-runner',
        'setuptools_scm',
        'setuptools_scm_git_archive',
    ],
    install_requires=[],
    tests_require=[
        'pytest',
    ],
    test_suite='tests',

    python_requires='>3.4',

    package_data={
        '': ['data/*']
    },

    classifiers=[
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
