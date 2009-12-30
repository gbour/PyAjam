Asterisk configuration
======================

You need to modify several files for asterisk to accept AJAM connections.
Usually, asterisk configuration files are in */etc/asterisk*

manager.conf
------------

::

   [general]
   enabled = yes
   webenabled = yes

::

   [admin]
   secret = admin
   deny=0.0.0.0/0.0.0.0
   permit=127.0.0.0/255.255.255.0
   read = system,call,log,verbose,command,agent,user,config
   write = system,call,log,verbose,command,agent,user,config

http.conf
---------

::

  [general]
  enabled=yes
  bindaddr=127.0.0.1
  bindport=8088
  prefix=asterisk

