#!/usr/bin/env python

import re
import sys

from setuptools import find_packages, setup

if sys.version_info < (3, 9, 0, 'final', 0):
    raise SystemExit('Python 3.9 or later is required!')

with open('README.rst', encoding='utf-8') as fd:
    long_description = fd.read()

with open('dynasor/__init__.py') as fd:
    lines = '\n'.join(fd.readlines())

version = re.search("__version__ = '(.*)'", lines).group(1)
maintainer = re.search("__maintainer__ = '(.*)'", lines).group(1)
url = re.search("__url__ = '(.*)'", lines).group(1)
license = re.search("__license__ = '(.*)'", lines).group(1)
description = re.search("__description__ = '(.*)'", lines).group(1)

# PyPI name
name = 'dynasor'

setup(name=name,
      version=version,
      description=description,
      long_description=long_description,
      url=url,
      maintainer=maintainer,
      platforms=['unix'],
      install_requires=[
          'ase',
          'mdanalysis',
          'numba>=0.55',
          'numpy>=1.18',
          'pandas>=2.2',
      ],
      scripts=['bin/dynasor'],
      packages=find_packages(),
      package_data={'': ['post_processing/neutron_scattering_lengths.json',
                         'post_processing/form-factors/*']},
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3 :: Only',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
          'Programming Language :: Python :: 3.11',
          'Programming Language :: Python :: 3.12',
          'Programming Language :: Python :: 3.13',
          'Intended Audience :: Education',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python',
          'Topic :: Scientific/Engineering :: Chemistry',
          'Topic :: Scientific/Engineering :: Physics',
      ])
