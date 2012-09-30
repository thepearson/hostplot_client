#!/usr/bin/env python

from distutils.core import setup

setup(name = "hostplot",
    version = "0.1",
    description = "Hostplot client application",
    long_description = "The hostplot.me client application to be run on hosts to gether metrics.",
    author = "craigp",
    author_email = 'craig@hostplot.me',
    url = "http://www.hostplot.me/client",
    download_url = "http://www.hostplot.me/client/download",
    platforms = ['any'],

    license = "GPLv3+",

    package_dir = {'myapp': 'src/myapp'},
    packages = ['myapp'],

    classifiers = [
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Development Status :: 5 - Production/Stable',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python'],
)
