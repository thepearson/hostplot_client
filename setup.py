#!/usr/bin/env python
import os
import subprocess

from distutils.core import setup, Command


class SetupBuildCommand(Command):
    """
    Master setup build command to subclass from.
    """

    user_options = []

    def initialize_options(self):
        """
        Setup the current dir.
        """
        self._dir = os.getcwd()

    def finalize_options(self):
        """
        Set final values for all the options that this command supports.
        """
        pass


#class TODOCommand(SetupBuildCommand):
    """
    Quick command to show code TODO's.
    """
    # See Figure 4
class SetupUsers(SetupBuildCommand):

  def run(self):
    cmd = ''


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

    package_dir = {'hostplot': 'src/client'},
    packages = ['hostplot'],

    classifiers = [
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Development Status :: 5 - Production/Stable',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python'],

    #cmdclass = {'name': CommandClass}
)
