#!/usr/bin/env python
# coding=utf-8
#
# Copyright © Splunk, Inc. All Rights Reserved.

from __future__ import absolute_import, division, print_function

import pathlib
import sys

from setuptools import find_packages, setup


if sys.version_info < (3, 5, 1):
    raise NotImplementedError('The ' + description + ' requires Python 3.5.1')

setup(
    name='dammy-splunk-packaging-toolkit',
    version='1.1.7-alpha',
    description='Dammy-Splunk Packaging Toolkit',
    long_description=pathlib.Path("README.txt").read_text(),
    long_description_content_type='text/markdown',
    url='https://dev.splunk.com',
    python_requires=">=3.5.1,<3.14",
    author='Splunk, Inc.',
    author_email='devinfo@splunk.com',
    license='https://www.splunk.com/en_us/legal/splunk-software-license-agreement.html',
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 5 - Production/Stable',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'License :: Other/Proprietary License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],

    packages=find_packages(exclude=["test", "test.*"]),
    package_data={
        'slim': [
            'config/conf-specs/*.spec',
            'config/common-information-models.json',
            'config/splunk-releases.json',
            'config/settings',
            'config/ignore',
            'man/man1/*.1'
        ],
    },
    include_package_data=True,
    data_files=[('', ['LICENSE.txt'])],
    install_requires=['semantic_version==2.8.5', 'future>=0.18.3', 'wheel==0.45.1', 'setuptools==75.6.0'],
    entry_points={'console_scripts': ['slim = slim.__main__:main']},
)
