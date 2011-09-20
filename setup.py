#!/usr/bin/env python
# -*- coding: utf8 -*-
__version__ = "$Revision$ $Date$"
__author__  = "Guillaume Bour <guillaume@bour.cc>"
__license__ = """
	Copyright (C) 2009-2011, Guillaume Bour <guillaume@bour.cc>

	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as
	published by the Free Software Foundation, version 3.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU Affero General Public License for more details.

	You should have received a copy of the GNU Affero General Public License
	along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from setuptools import setup, find_packages


setup(
	name              = "PyAjam",
	version           = "0.3",
	packages          = find_packages(),
  #install_requires  = ["4Suite-XML >= 1.0.2"],

	author            = "Guillaume Bour",
	author_email      = "guillaume@bour.cc",
	description       = "Python binding for Asterisk AJAM interface",
	license           = 'GNU General Public License v3',
	classifiers       = [
		'Development Status :: 4 - Beta',
		'Environment :: Console',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: GNU General Public License (GPL)',
		'Natural Language :: English',
		'Natural Language :: French',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		'Programming Language :: Python :: 2.5',
		'Programming Language :: Python :: 2.6',
		'Programming Language :: Python :: 2.7',
		'Topic :: Software Development',
		'Topic :: Software Development :: Libraries :: Python Modules',
		'Topic :: Utilities',
	],

	long_description  = """Pyajam allows to interact with an asterisk server using the AJAM interface, in a pythonic way""",

  tests_require     = "nose",
  test_suite        = "nose.collector",
	keywords          = "Asterisk AJAM API VoIP",
  url               = "http://devedge.bour.cc/wiki/Pyajam",
  download_url      = 'http://devedge.bour.cc/resources/pyajam/src/pyajam.latest.tar.gz',
)
