#!/usr/bin/env python

"""
========
setup.py
========

installs package

USAGE :
python setup.py install

Or for local installation:

python setup.py install --prefix=/your/local/dir

"""

import sys
try:
    from setuptools import setup, find_packages, Extension
except ImportError:
    from distutils.core import setup, find_packages, Extension
if (sys.version_info[0], sys.version_info[1]) != (3, 6):
    raise RuntimeError('Python 3.6.5 required ')

# main setup
setup(
    name='kipoi_gwas',
    author='Hackathon 2018',
    author_email='email@email.com',
    version='0.0.1',
    url='https://github.com/NCBI-Hackathons/Kipoi-GWAS',
    download_url='https://github.com/NCBI-Hackathons/Kipoi-GWAS/archive/master.zip',
    description='Kipoi analysis workflow for running Kipoi models',
    long_description='https://github.com/NCBI-Hackathons/Kipoi-GWAS/blob/master/README.md',
    keywords=['GWAS', 'deep-learning'],
    license='General Public License v. 3',
    install_requires=[
        'papermill',
    ],
    platforms='Tested on Ubuntu 16.04 64bit',
    packages=find_packages(),
    # package_data={'': ['beditor/data']},
    include_package_data=True,
    # entry_points={
    #    'console_scripts': ['beditor = beditor.pipeline:main',],
    #    },
)
