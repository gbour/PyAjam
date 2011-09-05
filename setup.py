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
	name              = "Pyajam",
	version           = "0.1.1",
	packages          = find_packages(),
	install_requires  = ["4Suite-XML >= 1.0.2"],

	author            = "Guillaume Bour",
	author_email      = "guillaume@bour.cc",
	description       = "blablabla",
	license           = "GPL3",
	keywords          = "asterisk ajam api",
	url               = "http://devedge.bour.cc/wiki/Pyajam",
)
