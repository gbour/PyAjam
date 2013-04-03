PyAjam
======

[AJAM](http://www.voip-info.org/wiki/view/Aynchronous+Javascript+Asterisk+Manager+%28AJAM%29) (Asynchronous Javascript Asterisk Manager) is the new interface build upon HTTP to interact with Asterisk. 
AJAM was Introduced in asterisk 1.4. Returned datas are mostly formatted in XML.

[PyAjam](http://devedge.bour.cc/wiki/PyAjam) is a python library allowing
programs to interact with an asterisk server using the AJAM interface, in
a pythonic way.


###Requirements:
* None 

###Compatility:
*	python 2.[5-7]

###Installation
	easy_install PyAjam

or

	wget http://devedge.bour.cc/resources/pyajam/src/pyajam.latest.tar.gz
	tar xvf pyajam.latest.tar.gz
	cd reblok-* && ./setup.py install

Features
--------

* retrieve basic informations (sip/iax2 peers, sip peer details, sip registry)
* catch asterisk events
* information presented in a pythonic way (dict)
* automatically reconnect to the asterisk server if connection lost
* compatible with asterisk 1.4, 1.6, 1.8, 10

Documentation
-------------

You can found PyAjam documentation at [http://devedge.bour.cc/resources/pyajam/doc/index.html](http://devedge.bour.cc/resources/pyajam/doc/index.html)

Example
-------

	>>> from pyajam import Pyajam

	>>> ajam = Pyajam(server='192.168.0.10', username='mspencer', password='*rocks!')
	>>> if not ajam.login():
	>>>		print "Invalid login"
	>>>		sys.exit(1)

	>>> # display list of peers (SIP and IAX2)
	>>> print ajam.peers())
	>>> # display peer 101 attributes
	>>> peer  = ajam.sippeer('101'))

	>>> # screenprint events
	>>> def ajam_event_listener(data):
	>>>		print data

	>>> ajam.waitevent(async=False, callback=ajam_event_listener)

About
-----

*PyAjam* is licensed under GNU GPL v3.
It is developped by Guillaume Bour <guillaume@bour.cc>
