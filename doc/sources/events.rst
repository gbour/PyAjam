Events
================

List of events that may be returned

PeerStatus
..........

triggered when a device is registering or unregistering

.. code-block:: python

   {
      u'event'     : u'PeerStatus'
      u'peer'      : u'SIP/101', 
      u'peerstatus': u'Registered',
      u'time'      : u'37'
      u'privilege' : u'system,all', 
   }

* **peer** pinpoint the device (PROTOCOL/identifiant)
* **peerstatus**: *Registered* or *Unregistered*, *Reachable*, *Unreachable*
* **time**: latency in milliseconds, only with peerstatus==Reacheable

Register: peer come to register to the asterisk server
Unregister: come to unregister

Reachable: triggered only if qualify option is set in sip.conf (either globally or for this peer)
Unreachable


time key only available when peerstatus == Reacheable|Unreachable
time = -1 when peerstatus == Unreachavle

WaitEventComplete
.................

{u'event': u'WaitEventComplete'}


Newchannel
..........

.. code-block:: python

   {
      u'event': u'Newchannel', 
      u'channel': u'SIP/101-086d58a8'
      u'uniqueid': u'1261087570.1', 
      u'calleridnum': u'101', 
      u'state': u'Down', 
      u'calleridname': u'<unknown>', 
      u'privilege': u'call,all', 
   }

device is opening a new channel


Newstate
........

.. code-block:: python

   {
      u'event': u'Newstate', 
      u'channel': u'SIP/101-086d58a8'
      u'uniqueid': u'1261087570.1', 
      u'state': u'Ring', 
      u'callerid': u'101', 
      u'calleridname': u'<unknown>', 
      u'privilege': u'call,all', 
   }


* state: Ring, Ringing, Up, Busy, Up

Device is entering a new state


Newexten
........

.. code-block:: python

  {
     u'event': u'Newexten', 
     u'channel': u'SIP/101-086d58a8'
     u'uniqueid': u'1261087570.1', 
     u'context': u'default', 
     u'extension': u'100', 
     u'priority': u'1', 
     u'application': u'NoOp', 
     u'appdata': u'exec 100', 
     u'privilege': u'call,all', 
  }

executing dialplan extension line


Hangup
......

.. code-block:: python

  {
    u'event': u'Hangup', 
    u'channel': u'SIP/101-086d4280'
    u'uniqueid': u'1261087819.2', 
    u'cause': u'21', 
    u'cause-txt': u'Call Rejected',
    u'privilege': u'call,all', 
  }

* cause
* cause-txt

NOTE: When 2 peers are bridged, Hangup event is triggered for both peers (channel key)


Dial
....

Dialing a peer

.. code-block:: python

   {
      u'event': u'Dial'
      u'srcuniqueid': u'1261088142.3', 
      u'destuniqueid': u'1261088142.4', 
      u'source': u'Console/dsp', 
      u'destination': u'SIP/101-086d4a00', 
      u'callerid': u'<unknown>', 
      u'calleridname': u'<unknown>', 
      u'privilege': u'call,all', 
   }


Newcallerid
...........


.. code-block:: python

   {
      u'event': u'Newcallerid', 
      u'channel': u'SIP/101-086d4a00'
      u'uniqueid': u'1261088142.4', 
      u'callerid': u'101', 
      u'calleridname': u'<Unknown>', 
      u'cid-callingpres': u'0 (Presentation Allowed, Not Screened)', 
      u'privilege': u'call,all', 
   }


Link
....

Both peers are bridged together (ie your call is accepted by the recipient)

.. code-block:: python

   {
      u'event': u'Link'
      u'uniqueid1': u'1261088142.3', 
      u'uniqueid2': u'1261088142.4', 
      u'channel1': u'Console/dsp',  
      u'channel2': u'SIP/101-086d4a00', 
      u'callerid1': u'',  
      u'callerid2': u'101', 
      u'privilege': u'call,all', 
   }


Call Rejected
.............
Peer device reject the call

.. code-block:: python

   {
      u'event': u'Hangup',  
      u'channel': u'SIP/101-086d4a00'
      u'uniqueid': u'1261088185.6', 
      u'cause': u'21', 
      u'cause-txt': u'Call Rejected', 
      u'privilege': u'call,all', 
   }


Reload
......


.. code-block:: python

   {
      u'event': u'Reload',
      u'message': u'Reload Requested', 
      u'privilege': u'system,all', 
   }

ChannelReload
.............

.. code-block:: python

   {
      u'event': u'ChannelReload', 
      u'channel': u'SIP', 
      u'reloadreason': u'RELOAD (Channel module reload)'
      u'user_count': u'1', 
      u'peer_count': u'1', 
      u'registry_count': u'0', 
      u'privilege': u'system,all', 
   }







