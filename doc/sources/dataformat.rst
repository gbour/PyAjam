Data format
===========

login
-----
.. code-block:: html

   >>> GET http://localhost:8088/asterisk/manager?action=login&username=foo&secret=bar


**login failed** response

.. code-block:: html

   <title>Asterisk&trade; Manager Interface</title>
   <body bgcolor="#ffffff">
     <table align=center bgcolor="#f1f1f1" width="500">
       <tr><td colspan="2" bgcolor="#f1f1ff"><h1>&nbsp;&nbsp;Manager Tester</h1></td></tr>
       <tr><td>Response</td><td>Error</td></tr>
       <tr><td>Message</td><td>Authentication failed</td></tr>
     </table>
   </body>


**login successed** response

.. code-block:: html

   <title>Asterisk&trade; Manager Interface</title>
   <body bgcolor="#ffffff">
     <table align=center bgcolor="#f1f1f1" width="500">
       <tr><td colspan="2" bgcolor="#f1f1ff"><h1>&nbsp;&nbsp;Manager Tester</h1></td></tr>
       <tr><td>Response</td><td>Success</td></tr>
       <tr><td>Message</td><td>Authentication accepted</td></tr>
     </table>
   </body>

HTTP headers sent back with html response. We have to remember *mansession_id* cookie for further queries::

  Server:	Asterisk/1.4.26.2
  Date:	Thu, 17 Dec 2009 20:57:31 GMT
  Connection:	close
  Cache-Control:	no-cache, no-store
  Content-Type:	text/html
  Set-Cookie:	mansession_id="44a02cf1"; Version="1"; Max-Age=60

Asterisk manager console display connected users::

  == HTTP Manager 'admin' logged on from 127.0.0.1
  *CLI> manager show connected
    Username         IP Address     
    admin            127.0.0.1  


show sip peers
--------------

http://localhost:8088/asterisk/mxml?action=sippeers

**invalid response** (not logged or timeout expired)

.. code-block:: xml

   <ajax-response>
     <response type='object' id='unknown'><generic response='Error' message='Authentication Required' /></response>
   </ajax-response>

.. code-block:: xml

   <ajax-response>
     <response type='object' id='unknown'><generic response='Success' message='Peer status list will follow' /></response>
     <response type='object' id='unknown'>
       <generic event='PeerEntry' channeltype='SIP' objectname='101' chanobjecttype='peer' 
                ipaddress='127.0.0.1' ipport='5061' dynamic='yes' natsupport='no' 
                videosupport='no' acl='no' status='Unmonitored' realtimedevice='no' />
     </response>
     <response type='object' id='unknown'><generic event='PeerlistComplete' listitems='1' /></response>
   </ajax-response>


Pyajam return

.. code-block:: python

   >>> print ajam.sippeers()
   [{ 
     u'acl': u'no',
     u'channeltype': u'SIP',
     u'chanobjecttype': u'peer',
     u'dynamic': u'yes',
     u'event': u'PeerEntry',
     u'ipaddress': u'127.0.0.1',
     u'ipport': u'5061',
     u'natsupport': u'no',
     u'objectname': u'101',
     u'realtimedevice': u'no',
     u'status': u'Unmonitored',
     u'videosupport': u'no'
   }]

