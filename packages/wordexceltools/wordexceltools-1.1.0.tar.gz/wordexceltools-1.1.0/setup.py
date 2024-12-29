#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
import sys
from shutil import rmtree

from setuptools import setup, Command

# Package meta-data.
NAME = 'wordexceltools'
DESCRIPTION = 'An efficient toolkit for handling Excel files and generating Word documents, leveraging the power of python-docx and openpyxl.'
URL = 'https://github.com/ldspdvsun/wordexceltools'
EMAIL = 'ldspdvsun@gmail.com'
AUTHOR = 'MengYue Sun'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = '1.1.0'

# What packages are required for this module to be executed?
REQUIRED = [
    'chardet==4.0.0', 'docx==0.2.4', 'openpyxl==3.1.5', 'python_docx==1.1.2',
]

# What packages are optional?
EXTRAS = {}

here = os.path.abspath(os.path.dirname(__file__))

try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass
        os.system('{0} setup.py sdist bdist_wheel'.format(sys.executable))
        os.system('twine upload dist/*')
        sys.exit()

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=['wordexceltools'],
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license='Apache',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
    cmdclass={
        'upload': UploadCommand,
    },
)
