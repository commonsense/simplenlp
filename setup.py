#!/usr/bin/env python

"""
Simple, multilingual natural language tools.

This package accomplishes many basic NLP tasks without dependencies on NLTK or parsers, for use in projects such as ConceptNet.
"""

version_str = '1.0.0'

try:
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup, Extension
import os.path, sys
from stat import ST_MTIME

classifiers=[
    'Intended Audience :: Developers',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: GNU General Public License (GPL)',
    'Natural Language :: English',
    'Operating System :: MacOS',
    'Operating System :: Microsoft :: Windows',
    'Operating System :: POSIX',
    'Operating System :: Unix',
    'Programming Language :: C',
    'Programming Language :: Python :: 2.5',
    'Programming Language :: Python :: 2.6',
    'Topic :: Scientific/Engineering',
    'Topic :: Software Development',
    'Topic :: Text Processing :: Linguistic',]

doclines = __doc__.split("\n")

setup(
    name="simplenlp",
    version=version_str,
    maintainer='MIT Media Lab, Software Agents group',
    maintainer_email='conceptnet@media.mit.edu',     
    url='http://csc.media.mit.edu/',
    license = "http://www.gnu.org/copyleft/gpl.html",
    platforms = ["any"],
    description = doclines[0],
    classifiers = classifiers,
    long_description = "\n".join(doclines[2:]),
    packages=['simplenlp', 'simplenlp.en', 'simplenlp.ar', 'simplenlp.es',
              'simplenlp.fi', 'simplenlp.fr', 'simplenlp.hu', 'simplenlp.it',
              'simplenlp.ja', 'simplenlp.ko', 'simplenlp.mblem',
              'simplenlp.nl', 'simplenlp.pt', 'simplenlp.zh'],
    install_requires=['csc-utils >= 0.6'],
    package_data={'simplenlp': ['mblem/*.pickle', 'en/*.txt', 'es/stop.txt',
                                'hu/stop.txt', 'nl/stop.txt', 'pt/stop.txt']}
)
