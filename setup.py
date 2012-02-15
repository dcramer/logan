#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='logan',
    version='0.1.0',
    author='David Cramer',
    author_email='dcramer@gmail.com',
    url='http://github.com/dcramer/logan',
    description='Logan is a toolkit for building standalone Django applications.',
    packages=find_packages(exclude=["example_project", "tests"]),
    zip_safe=False,
    install_requires=[],
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
