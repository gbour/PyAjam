from setuptools import setup, find_packages


setup(
	name 							= "Pyajam",
	version 					= "0.1",
	packages 					= find_packages(),
	install_requires 	= ["4Suite-XML >= 1.0.2"],

	author 						= "Guillaume Bour",
	author_email 			= "guillaume@bour.cc",
	description 			= "blablabla",
	license 					= "GPL3",
	keywords 					= "asterisk ajam api",
	url 							= "http://devedge.bour.cc/wiki/Pyajam",
)
