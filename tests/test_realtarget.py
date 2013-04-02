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
import argparse

from pyajam import Pyajam

class BaseTest(unittest.TestCase):
    def __init__(self, name, (server, user, password), version, login=False):
        super(BaseTest, self).__init__(name)

        self.server  = server
        self.user    = user
        self.pwd     = password
        self.version = version

        self.login   = login

    def setUp(self):
        self.ajam = Pyajam(server=self.server, username=self.user, password=self.pwd)

        if self.login:
            self.ajam.login()


class TestLogin(BaseTest):
    def __init__(self, *args, **kwargs):
        super(TestLogin, self).__init__(*args, **kwargs)

        #self.path = os.path.join(os.getcwd(), "traces", version)

    def tearDown(self):
        self.ajam = None

    def test_login(self):
        self.assertTrue(self.ajam.login())
        self.assertEqual(self.ajam.version(), self.version)
        #self.assertEqual(self.ajam._sessionid_, '3ac1e27b')

class TestAPI(BaseTest):
    def __init__(self, *args, **kwargs):
        super(TestAPI, self).__init__(*args, **kwargs)

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
    parser = argparse.ArgumentParser(description='Test pyajam library on real asterisk server')
    parser.add_argument('-s', '--server'  , default='localhost', help='Asterisk server to launch test on')
    parser.add_argument('-u', '--user'    , default='admin'    , help='AMI user')
    parser.add_argument('-p', '--password', default='admin'    , help='AMI password')
    parser.add_argument('-v', '--version' , default='1.4'      , help='Asterisk version')
    args = parser.parse_args()

    suite = unittest.TestSuite()
    testnames =  unittest.TestLoader().getTestCaseNames(TestLogin)
    for name in testnames:
        suite.addTest(TestLogin(name, (args.server, args.user, args.password), args.version))

    testnames =  unittest.TestLoader().getTestCaseNames(TestAPI)
    for name in testnames:
        suite.addTest(TestAPI(name, (args.server, args.user, args.password), args.version, login=True))
        suite.addTest(TestAPI(name, (args.server, args.user, args.password), args.version, login=False))

    unittest.TextTestRunner(verbosity=2).run(suite)

