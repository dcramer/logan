#!/usr/bin/env python
"""
Logan
======

Logan is a toolkit for running standalone Django applications. It provides you
with tools to create a CLI runner, manage settings, and the ability to bootstrap
the process.

:copyright: (c) 2012 David Cramer.
:license: Apache License 2.0, see LICENSE for more details.
"""
from setuptools import setup, find_packages

setup(
    name='logan',
    version='0.1.0',
    author='David Cramer',
    author_email='dcramer@gmail.com',
    url='http://github.com/dcramer/logan',
    description='Logan is a toolkit for building standalone Django applications.',
    packages=find_packages(exclude=["tests"]),
    long_description=__doc__,
    zip_safe=False,
    install_requires=[],
    tests_require=[
        'django>=1.2.5,<1.4',
        'nose>=1.1.2',
        'unittest2',
    ],
    license='Apache License 2.0',
    include_package_data=True,
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
)
