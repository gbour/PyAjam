.. Pyajam documentation master file, created by
   sphinx-quickstart on Thu Dec 17 11:00:23 2009.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

:mod:`pyajam` --- python **Asterisk AJAM** interface
====================================================

.. module:: pyajam
   :synopsys: python interface to Asterisk AJAM API

.. sectionauthor:: Guillaume Bour <guillaume@bour.cc>

The purpose of pyajam is to allow python programs interact with an asterisk 
server.

.. code-block:: python

  ajam = Pyajam(username='mspencer', password='*rocks!')
  if not ajam.login():
    print "Invalid login"
    sys.exit(1)

  peers = ajam.peers())          # array of SIP/IAX2 peers
  peer  = ajam.sippeer('101'))   # dictionary of peer attributes

  # screenprint events
  def ajam_event_listener(data):
    print data

  ajam.waitevent(async=False, callback=ajam_event_listener)

.. toctree::
   :maxdepth: 2
   :numbered:

   sources/asteriskconf.rst
   sources/dataformat.rst
   sources/events.rst
   sources/about.rst

Modules
=======

.. automodule:: pyajam
   :members:

.. autoclass:: pyajam.Pyajam
   :members:

Changelog
=========

* v0.1: initial release
