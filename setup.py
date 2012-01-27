#!/usr/bin/env python

languages = ['ar', 'en', 'es', 'fi', 'fr', 'hu', 'it', 'ja', 'ja_cabocha', 'ko', 'nl', 'pt', 'ru', 'zh']
packages = ['simplenlp', 'simplenlp.default', 'simplenlp.mblem'] + ['simplenlp.'+lang for lang in languages]

version_str = '1.1.1'

try:
    from setuptools import setup, find_packages

    # Verify the list of packages.
    setuptools_packages = find_packages(exclude=[])
    if set(packages) != set(setuptools_packages):
        import sys
        print >>sys.stderr, 'Missing or extraneous packages found.'
        print >>sys.stderr, 'Extraneous:', list(set(packages) - set(setuptools_packages))
        print >>sys.stderr, 'Missing:', list(set(setuptools_packages) - set(packages))
        raw_input()

except ImportError:
    from distutils.core import setup

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

import os
README_contents = open(os.path.join(os.path.dirname(__file__), 'README.txt')).read()
doclines = README_contents.split("\n")

setup(
    name="simplenlp",
    version=version_str,
    maintainer='MIT Media Lab, Software Agents group',
    maintainer_email='conceptnet@media.mit.edu',     
    url='http://github.com/commonsense/simplenlp/',
    license = "http://www.gnu.org/copyleft/gpl.html",
    platforms = ["any"],
    description = doclines[0],
    classifiers = classifiers,
    long_description = "\n".join(doclines[2:]),
    packages=packages,
    install_requires=['csc-utils >= 0.6'],
    package_data={'simplenlp': ['mblem/*.pickle', 'en/*.txt', 'es/*.txt',
                                'hu/stop.txt', 'nl/stop.txt', 'pt/stop.txt']}
)
