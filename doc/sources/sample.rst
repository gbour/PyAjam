Example
=======

.. code-block:: python

  ajam = Pyajam(username='mspencer', password='*rocks!', autoconnect=True, unify=True)
  if not ajam.login():
    print "Invalid login"
    sys.exit(1)

  peers = ajam.sippeers())
  #pp.pprint(ajam.sipregistry())
  #pp.pprint(ajam.sippeer('101'))

  def ajam_event_listener(data):
    print "event data >>>"
    print data[1]
    print "<<<"

  print ajam.waitevent(ajam_event_listener, True)


