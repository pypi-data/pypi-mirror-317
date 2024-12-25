#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
from setuptools import setup, find_packages

MAJOR = 2
MINOR = 0
PATCH = 7
VERSION = f"{MAJOR}.{MINOR}.{PATCH}"


def get_install_requires():
    reqs = [
        'fsspec == 2024.10.0',
        'polars == 1.16.0',
        'pydantic == 2.10.4',
        'aiofiles == 24.1.0',
        'aiolimiter == 1.2.1',
        'tqdm == 4.67.1',
        'cachetools == 5.5.0',
        'diskcache == 5.6.3',
        'tenacity == 9.0.0',
        'apscheduler == 3.11.0',
        'pandas == 2.2.3'
    ]
    return reqs


setup(
    name="py_rtf_framework",
    version=VERSION,
    author="liupeng",
    author_email="895876294@qq.com",
    long_description_content_type="text/markdown",
    url='',
    long_description=open('README.md', encoding="utf-8").read(),
    python_requires=">=3.12",
    install_requires=get_install_requires(),
    packages=find_packages(),
    license='Apache',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    package_data={'': ['*.csv', '*.txt', '.toml']},  # 这个很重要
    include_package_data=True
)
