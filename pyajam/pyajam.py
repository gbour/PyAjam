# -*- coding: utf8 -*-
"""
    pyajam, ...
    Copyright (C) 2009	Guillaume Bour <guillaume@bour.cc>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
__author__  = "Guillaume Bour <guillaume@bour.cc>"
__status__  = "developpement"
__version__ = "0.1"
__date__    = "2009/12/17"


import sys, urllib2, re, logging, httplib, time

# only on python 2.5 & superior
if not hasattr(urllib2, 'quote'):
	import urllib
	urllib2.quote = urllib.quote


class Pyajam:

	def __init__(self, server='localhost', port=8088, path='/asterisk', 
						   username='admin', password='admin', autoconnect=True, 
							 asraw=False):
		"""Pyajam initialisation.

     Parameters:
      * **server**: adress or IP of the asterisk server to connect to (default= *localhost*),
      * **port**: ajam port (as defined in `asterisk/http.conf <http://www.voip-info.org/wiki/index.php?page=Asterisk+config+http.conf>`_),
      * **path**: url path to send ajam queries,
      * **username**: ajam login username (as defined in `asterisk/manager.conf <http://www.voip-info.org/tiki-index.php?page=Asterisk%20config%20manager.conf>`_),
      * **password**: ajam login password,
      * **autoconnect**: Pyajam automatically (re)connect to AJAM server,
      * **raw**: return values as raw (e.g not pythonified)
		"""
		self.url					=	"http://%s:%d%s" % (server, port, path)
		self.username			= username
		self.password			= password
		self.autoconnect	= autoconnect
		self.unify				= not asraw

		self._sessionid_ 	= ''
		self._version_		= None

	def _query(self, mode, action, args={}):
		"""Query Asterisk AJAM service.

		"""
		qargs = '&'.join(map(lambda x: "%s=%s" % (x, urllib2.quote(args[x])), args))
		if len(qargs) > 0:
			qargs = '&' + qargs

		logging.debug("GET %s/%s?action=%s%s" % (self.url, mode, action, qargs))
		req = urllib2.Request("%s/%s?action=%s%s" % (self.url, mode, action, qargs))
		req.add_header('Cookie', "mansession_id=\"%s\"" % self._sessionid_)
		try:
			f = urllib2.urlopen(req)		
			data = f.read()
			logging.debug(data)
		except Exception, e:
			logging.error(e)
			return (None, None)

		if self.autoconnect and \
	     ('Authentication Required' in data or 'Permission denied' in data):
			logging.debug('trying to reconnect...')
			if not self.login():
				return (None, None)

			req.add_header('Cookie', "mansession_id=\"%s\"" % self._sessionid_)
			try:
				f = urllib2.urlopen(req)
				data = f.read()
			except Exception, e:
				return (None, None)
		
		return (f.info(), data)
	
	def _unify_xml(self, raw, normalizer=None, xpath=u'(//generic[@event])'):
		"""Convert Asterisk ajam XML message to python dictionary.
		"""
		from Ft.Xml.Domlette import NonvalidatingReader
		from Ft.Xml.XPath import Evaluate
		from Ft.Xml.XPath.Context import Context

		doc 		= NonvalidatingReader.parseString(raw)
		datas		= []

		for event in doc.xpath(xpath):
			attrs = {}

			for key in event.attributes.keys():
				attrs[key[1]] = event.attributes[key].value

			if normalizer:
				attrs = normalizer(attrs)
			if attrs:
				datas.append(attrs)

		return datas
		
	def _unify_raw(self, raw, regex, normalizer, datas=[]):
		"""Convert Asterisk raw message (old manager API) to python dictionary.
		"""
		if regex is None:
			return raw

		if type(regex) == str:
			regex = re.compile(regex, re.M)

#		datas = []
		for m in regex.finditer(raw):
			obj = m.groupdict()

			if normalizer:
				obj = normalizer(obj)

			if obj:
				if isinstance(datas, list):
					datas.append(obj)
				elif isinstance(datas, dict):
					datas.update(obj)

		return datas

	def login(self):
		"""Login to Asterisk AJAM service.
 		 Use the username & password provided at class instantiation.

		 Returns **True** if login success, else **False**
		"""
		(info, data) = self._query('manager', 'login', 
 			{'username': self.username, 'secret': self.password})
		if not info or not "Authentication accepted" in data:
			self._sessionid_ = ''
			return False

		# setting session
		#print f.info()
		self._sessionid_ = info['set-cookie'].split(';')[0].split('=')[1][1:-1]

		# extraction asterisk version
		if not info.has_key('Server') or \
		not info['Server'].startswith('Asterisk/'):
			logging.error("login:: not logging to an asterisk server")
			return False

		self._version_ = info['Server'].split('/')[1][:3]
#		print 'version=', self._version_
		if self._version_ not in ['1.4', '1.6']:
			logging.error("login:: Unmanaged %s asterisk version" % self._version_)
			return 'False'
		
		return True

	def version(self):
		"""Return Asterisk version of server you are connected to.
	   Values are **None** (not connected), **1.4** or **1.6**.
		"""
		return self._version_

	def sippeers(self):
		"""Query SIP peers definition.
     Return list of peers (each peer is represented as a dictionary).

     Useful items are:
       * **objectname**, the peer name
       * **status**, with *OK* value if peer is connected
       * **ipaddress**, device IP

     New fields in asterisk 1.6:
       * **textsupport**

     ::

     # sippeers() output sample
     >>> import pprint
     >>> from pyajam import Pyajam
     >>> ajam = Pyajam(username='mspencer', password='*rocks!')
     >>> pprint.pprint(ajam.sippeers())
     [ { u'acl'           : u'no',
         u'channeltype'   : u'SIP',
         u'chanobjecttype': u'peer',
         u'dynamic'       : u'yes',
         u'event'         : u'PeerEntry',
         u'ipaddress'     : u'-none-',
         u'ipport'        : u'0',
         u'natsupport'    : u'no',
         u'objectname'    : u'102',
         u'realtimedevice': u'no',
         u'status'        : u'UNKNOWN',
         u'videosupport'  : u'no',
         u'textsupport'   : u'no'},
       { u'acl'           : u'no',
         u'channeltype'   : u'SIP',
         u'chanobjecttype': u'peer',
         u'dynamic'       : u'yes',
         u'event'         : u'PeerEntry',
         u'ipaddress'     : u'127.0.0.1',
         u'ipport'        : u'5061',
         u'latency'       : u'1',
         u'natsupport'    : u'no',
         u'objectname'    : u'101',
         u'realtimedevice': u'no',
         u'status'        : u'OK',
         u'videosupport'  : u'no',
         u'textsupport'   : u'no'}]
		"""
		(info, data) = self._query('mxml', 'sippeers')
		if not info:
			return False

		if self.unify:
			def _normalize(row):
				if row['event'] != 'PeerEntry':
					return None

				# when OK, status = 'OK (13 ms)' per example (with latency in parenthesis)
				if row['status'][0:2] == 'OK':
					row[u'latency']	= row['status'][4:-4]
					row[u'status'] 	= u'OK'

				return row

			data = self._unify_xml(data, _normalize)
			#data = self._unify_xml(data, lambda r: r['event'] == 'PeerEntry' and r or None)
		return data

	def iaxpeers(self):
		"""Query IAX peers definition.
     Return list of peers (each peer is represented as a dictionary).

     Useful items are:
       * **objectname**, the peer name
       * **status**, with *OK* value if peer is connected
       * **ipaddress**, device IP

     New fields in asterisk 1.6:
       * **chanobjecttype**
       * **encryption**
       * **event**
       * **trunk**

     Notes:
       * **username** field is truncated if longer than 10 characters

     ::

     # iaxpeers() output sample
     >>> import pprint
     >>> from pyajam import Pyajam
     >>> ajam = Pyajam(username='mspencer', password='*rocks!')
     >>> pprint.pprint(ajam.IAXpeers())
     [ { u'channeltype'   : u'IAX2',
         u'dynamic'       : u'no',
         u'ipaddress'     : u'216.207.245.47',
         u'ipport'        : u'4569',
         u'objectname'    : u'demo',
         u'username'      : u'asterisk',
         u'status'        : u'Unmonitored',
         u'chanobjecttype': u'peer',
         u'encryption'    : u'no',
         u'event'         : u'PeerEntry',
         u'trunk'         : u'no'}]


		"""
		mode = 'rawman'
		if self._version_ == '1.6':
			mode = 'mxml'
		(info, data) = self._query(mode, 'iaxpeers')

		if not info:
			return False

		if self.unify:
			def _normalize(row):
				row[u'channeltype'] = u'IAX2'
		
				if row['dynamic'] == 'D':
					row['dynamic'] = u'yes'
				else:
					row['dynamic'] = u'no'
		
				# when OK, status = 'OK (13 ms)' per example
				if row['status'][0:2] == 'OK':
					row[u'latency']	= row['status'][4:-4]
					row[u'status'] 	= 'OK'

				name = row['objectname'].split('/')
				if len(name) > 1:
					row[u'objectname'] 	= name[0]
					row[u'username']	  = name[1]
				else:
					row[u'username']		= u''

				return row

		if self._version_ == '1.6':
			data = self._unify_xml(data, _normalize)
		else:
			data = self._unify_raw(data, 
				'^(?P<objectname>[^\s]+)\s+(?P<ipaddress>[0-9.]*)\s+\\((?P<dynamic>S|D)\\)\s+([0-9.]+)\s+(?P<ipport>\d+)\s+(?P<status>.*?)\s+$',
				_normalize
			)
		return data

	def peers(self):
		"""Query both IAX and SIP peers.
     Return list of peers (each peer is represented as a dictionary).
     Use **channeltype** to distinguish between *sip* and *iax2* devices.
     ::

     # peers() output sample
     >>> import pprint
     >>> from pyajam import Pyajam
     >>> ajam = Pyajam(username='mspencer', password='*rocks!')
     >>> pprint.pprint(ajam.peers())
     [ { u'channeltype'   : u'IAX2',
         u'chanobjecttype': u'peer',
         u'dynamic'       : u'no',
         u'encryption'    : u'no',
         u'event'         : u'PeerEntry',
         u'ipaddress'     : u'-none-',
         u'ipport'        : u'0',
         u'objectname'    : u'iax1',
         u'status'        : u'Unmonitored',
         u'trunk'         : u'no',
         u'username'      : u''},
       { u'acl'           : u'no',
         u'channeltype'   : u'SIP',
         u'chanobjecttype': u'peer',
         u'dynamic'       : u'yes',
         u'event'         : u'PeerEntry',
         u'ipaddress'     : u'127.0.0.1',
         u'ipport'        : u'5061',
         u'latency'       : u'1',
         u'natsupport'    : u'no',
         u'objectname'    : u'101',
         u'realtimedevice': u'no',
         u'status'        : u'OK',
         u'textsupport'   : u'no',
         u'videosupport'  : u'no'}]
		"""
		peers = self.sippeers()
		peers.extend(self.iaxpeers())

		return(peers)

	def sipregistry(self):
		"""Query SIP devices registration status
     (mainly used for trunks).

     New fields in asterisk 1.6:
       * **event**
       * **registrationtime**

     ::

     # sipregistry() output sample
     >>> import pprint
     >>> from pyajam import Pyajam
     >>> ajam = Pyajam(username='mspencer', password='*rocks!')
     >>> pprint.pprint(ajam.sipregistry())
     [ { u'event': u'RegistryEntry',
         u'host'            : u'mysipprovider.com',
         u'port'            : u'5060',
         u'refresh'         : u'120',
         u'registrationtime': u'0',
         u'state'           : u'Unregistered',
         u'username'        : u'1234'}]
		"""
		if self._version_ == '1.6':
			def _normalize(row):
				if row['event'] != 'RegistryEntry':
					return None
				return row

			(info, data) = self._query('mxml', 'sipshowregistry')
			if not info:
				return False

			data = self._unify_xml(data, _normalize)
		else:
			data = self.command('sip show registry',
				'^(?P<host>[^\s]+):(?P<port>[0-9]+)\s+(?P<username>[^\s]+)\s+(?P<refresh>[0-9.]+)\s+(?P<state>[^\s]+).*$'
			)

		return data

#			raw command: sip show peer <peername>
#			Note: keys are lowered
	def sippeer(self, peername):
		"""Query details about a SIP peer.
		 Comparing to sippeers(), here you have got detailed informations about the peer.

     New fields in asterisk 1.6:
       * a lot of fields have been renamed or added between 1.4 and 1.6

     ::

     # sippeer() output sample
     >>> import pprint
     >>> from pyajam import Pyajam
     >>> ajam = Pyajam(username='mspencer', password='*rocks!')
     >>> pprint.pprint(ajam.sippeer('101'))
     { 'acl'          : 'No',
       'addr->ip'     : '127.0.0.1 Port 5061',
       'ama flags'    : 'Unknown',
       'auto-framing' : 'No',
       'call limit'   : '0',
       'callerid'     : '"" <>',
       'callgroup'    : '',
       'callingpres'  : 'Presentation Allowed, Not Screened',
       'canreinvite'  : 'Yes',
       'codec order'  : '(none)',
       'codecs'       : '0x8000e (gsm|ulaw|alaw|h263)',
       'context'      : 'default',
       'def. username': '101',
       'defaddr->ip'  : '0.0.0.0 Port 5060',
       'dtmfmode'     : 'rfc2833',
       'dynamic'      : 'Yes',
       'expire'       : '1801',
       'insecure'     : 'no',
       'language'     : '',
       'lastmsg'      : '0',
       'lastmsgssent' : '32767/65535',
       'mailbox'      : '',
       'maxcallbr'    : '384 kbps',
       'md5secret'    : '<Not set>',
       'name'         : '101',
       'nat'          : 'RFC3581',
       'overlap dial' : 'No',
       'pickupgroup'  : '',
       'promiscredir' : 'No',
       'reg. contact' : 'sip:101@127.0.0.1:5061',
       'secret'       : '<Not set>',
       'send rpid'    : 'No',
       'sip options'  : '(none)',
       'status'       : 'OK (1 ms)',
       'subscr.cont.' : '<Not set>',
       'subscriptions': 'Yes',
       't38 pt udptl' : 'No',
       'tohost'       : '',
       'transfer mode': 'open',
       'trust rpid'   : 'No',
       'user=phone'   : 'No',
       'useragent'    : 'Twinkle/1.4.2',
       'video support': 'No',
       'vm extension' : 'asterisk'}

		"""
		if self._version_ == '1.6':
			(info, data) = self._query('mxml', 'sipshowpeer', {'peer': peername})
			if not info:
				return False

			data = self._unify_xml(data, xpath=u'(//generic[@response])')
		else:
			def _normalizer(row):
				key = row['key'].strip()
				if key in ['Response', 'Privilege']:
					return None

				if key == '* Name':	
					key = 'Name'

				row[key.lower()] = row['value'].strip()

				del row['key']
				del row['value']
				return row

			data = self.command('sip show peer ' + peername,
				'^(?P<key>.*?):(?P<value>.*)$',
				_normalizer, {}
			)
		return data
		

	def command(self, command, regex=None, normalizer=None, unifyin=[]):
		"""Execute an Asterisk command.
			command is always returned in raw mode from asterisk.
      *command* is the asterisk command as typed in asterisk console,
      *regex* is a python regular expression use to parse command returned value,
      *normalizer* is used to normalize returned results
      *unifyin* is either an empty list or dict, as you want to return a list or a dict

     ::

     # direct call command() output sample
     >>> import pprint, re
     >>> from pyajam import Pyajam
     >>> ajam = Pyajam(username='mspencer', password='*rocks!')
     >>> 
     >>> rx = re.compile('^(?P<key>[^\s]+)\s+(?P<value>.*?)\s+\s+.*$', re.M)
     >>> def module_show_normalize(row):
     ...   if row['key'] in ('--END', 'Response:', 'Privilege:', 'Module') or \\
     ...      row['value'] == 'modules':
     ...   return None
     ...
     ...   row[row['key']] = row['value']
     ...   del row['key']
     ...   del row['value']
     ...
     ...   return row
     ...
     >>> pprint.pprint(ajam.command('module show', rx, module_show_normalize))
     [{'res_features.so': 'Call Features Resource'},
      {'res_musiconhold.so': 'Music On Hold Resource'},
      {'pbx_config.so': 'Text Extension Configuration'},
      {'chan_sip.so': 'Session Initiation Protocol (SIP)'},
      {'app_ldap.so': 'LDAP directory lookup function for Aster 0'}]

		"""
		(info, data) = self._query('rawman', 'command', {'command': command})
		if not info:
			return False

		if self.unify and regex:
			data = self._unify_raw(data, regex, normalizer, unifyin)
		return data

	def waitevent(self, async=False, callback=None):
		"""Manage Asterisk events.
        If *async* is True, execute callback function when receiving events, else return event datas,
        *callback* is the called function called in async mode.

      **Callback function**:
        the callback function must take one argument. This argument is an array of
        events (dictionary)

     ::

     # waitevent() output sample
     >>> import pprint, re
     >>> from pyajam import Pyajam
     >>> ajam = Pyajam(username='mspencer', password='*rocks!')
     >>> pprint ajam.waitevent(async=False)
     >>>
     >>> def ajam_event_listener(data):
     >>>   pp.pprint(data[1])
     >>> ajam.waitevent(async=True, callback=ajam_event_listener)
     [ { u'event': u'Reload',
         u'message': u'Reload Requested',
         u'privilege': u'system,all'},
        {u'event': u'WaitEventComplete'}]
		"""
		if async:
			if not callback:
				raise ValueError('callback argument is required when async is true')

			from Queue import Queue
			import thread
			self.eventQ = Queue(0)
			thread.start_new_thread(self._waitevent_wait, (callback,))

		self._waitevt__run = True
		while self._waitevt__run:
			(info, data) = self._query('mxml', 'waitevent')
			if not info:
				time.sleep(1); continue
		
			if async:
				self.eventQ.put_nowait(data)
			elif callback:
				try:
					if self.unify:
						data = self._unify_xml(data)

					callback(data)
				except Exception, e:
					print e
			else:
				return data
			

	def waitevent_stop():
		"""Stop event async manager.
		"""
		self._waitevt__run = False

	def _waitevent_wait(self, callback):
		"""Event async manager.
		"""
		while self._waitevt__run:
			try:
				data = self.eventQ.get()
				if self.unify:
					data = self._unify_xml(data)

				callback(data)
			except Exception:
				pass

if __name__ == '__main__':
	logging.basicConfig(level=logging.ERROR)

	import pprint
	pp = pprint.PrettyPrinter(indent=2)

	ajam = Pyajam()
	if not ajam.login():
		print "Invalid login"
		sys.exit(1)

	print 'asterisk version=', ajam.version()
	# Get SIP peers list
	pp.pprint(ajam.sippeers())
	# Get IAX2 peers list
	pp.pprint(ajam.iaxpeers())
	# Get SIP+IAX2 peers list
	pprint.pprint(ajam.peers())
	# Get SIP registry
	pp.pprint(ajam.sipregistry())
	# Get SIP peer 101
	pp.pprint(ajam.sippeer('101'))

	# Get modules list
	rx = re.compile('^(?P<key>[^\s]+)\s+(?P<value>.*?)\s+\s+.*$', re.M)
	def module_show_normalize(row):
		if row['key'] in ('--END', 'Response:', 'Privilege:', 'Module') or row['value'] == 'modules':
			return None

		row[row['key']] = row['value']
		del row['key']
		del row['value']
	
		return row
	pprint.pprint(ajam.command('module show', rx, module_show_normalize))

	# Event handler
	def ajam_event_listener(data):
		print "event data >>>"
		pp.pprint(data)

	ajam.waitevent(True, ajam_event_listener)
