# -*- coding: utf8 -*-
# vim:syntax=python:sw=4:ts=4:expandtab
"""
    pyajam, Python Asterisk AJAM binding
    Copyright (C) 2009-2012  Guillaume Bour <guillaume@bour.cc>

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
import unittest
import os
import os.path

from pyajam import Pyajam


def fake_query(_path, _action):
    """We fake the code querying Asterisk AJAM interface

        _qq() read the file traces/${ersion}/${action}
        this file must contains what AJAM would return (including status code and HTTP headers)
    """
    def _qq(mode, action, args={}):        
        headers = dict()
        content = None

        if action == 'command':
            action = args['command']

        with open(os.path.join(_path, action)) as f:
            # first line is HTTP 
            f.readline()

            while True:
                l = f.readline()
                if l == '\r\n':
                    break

                (key, value) = l[:-1].split(':', 1)
                if key.lower() == 'set-cookie':
                    key = key.lower()
                headers[key] = value.strip()

            content = f.read()
        return (headers, content)
    return _qq

class TestDecoding(unittest.TestCase):
    def __init__(self, name, version=None):
        super(TestDecoding, self).__init__(name)
        self.version = version
        self.path = os.path.join(os.getcwd(), "traces", version)

    def setUp(self):
        self.ajam = Pyajam()
        self.ajam._query = fake_query(self.path, self._testMethodName.split('_')[1])

        # we *force* asterisk version in ajam (note if we run *test_login*, will be replaced by real version)
        self.ajam._version_ = self.version

    def tearDown(self):
        self.ajam = None

    def test_login(self):
        self.assertTrue(self.ajam.login())
        self.assertEqual(self.ajam.version(), self.version)
        self.assertEqual(self.ajam._sessionid_, '3ac1e27b')

    def test_sippeers(self):
        peers = self.ajam.sippeers()
        self.assertEqual(len(peers), 2)
        self.assertTrue(peers[0].get('objectname', 'none') in ['101','102'])

    def test_iaxpeers(self):
        peers = self.ajam.iaxpeers()
        self.assertEqual(len(peers), 1)
        self.assertEqual(peers[0].get('objectname','none'), 'demo')

    def test_peers(self):
        peers = self.ajam.peers()
        self.assertEqual(len(peers), 3)
        self.assertEqual(len([x for x in peers if x['channeltype'] == 'SIP']), 2)
        self.assertEqual(len([x for x in peers if x['channeltype'] == 'IAX2']), 1)

    def test_sipregistry(self):
        regs = self.ajam.sipregistry()
        self.assertEqual(len(regs), 1)
        self.assertEqual(regs[0]['username'], 'myISP')

    def test_peer(self):
        peer = self.ajam.sippeer('101')
        self.assertTrue(isinstance(peer, dict))
        self.assertEqual(peer.get('objectname',None), '101')
        self.assertEqual(peer.get('status',None), 'Unmonitored')


if __name__ == '__main__':
    testnames =  unittest.TestLoader().getTestCaseNames(TestDecoding)

    for vers in ['1.4', '1.6']:
        print "** with asterisk %s **" % vers

        suite = unittest.TestSuite()
        for name in testnames:
            suite.addTest(TestDecoding(name, vers))

        unittest.TextTestRunner(verbosity=2).run(suite)

