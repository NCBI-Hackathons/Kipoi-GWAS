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
keywords=['GWAS','deep-learning'],
license='General Public License v. 3',
#install_requires=['biopython==1.71',
#                  'regex==2018.7.11',
#                    'pandas == 0.23.3',
#                    # 'pyyaml',
#                    'numpy==1.13.1',
#                    'matplotlib==2.2.2',
#                    'pysam==0.14.1',
#                    'requests==2.19.1',
#                    'scipy==1.1.0',
#                    'tqdm==4.23.4',
#                    'seaborn==0.8.1',
                    # 'pyensembl==1.4.0',
#                      'datacache==1.1.4',
#                     'dna_features_viewer==0.1.9',
#                    ],
platforms='Tested on Ubuntu 16.04 64bit',
packages=find_packages(),
#package_data={'': ['beditor/data']},
include_package_data=True,
#entry_points={
#    'console_scripts': ['beditor = beditor.pipeline:main',],
#    },
)
