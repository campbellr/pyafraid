""" This module tests the afaid.py module
"""
import unittest2

from mock import patch, Mock

import afraid

class TestAfraid(unittest2.TestCase):
    @patch('sys.exit')
    def test_error(self, mockexit):
        """ Test that the error method works properly
        """
        errcode = 2
        afraid.error('this is an error message', code=errcode)
        mockexit.assert_called_with(2)

    def test_get_sha(self):
        """ Test that the get_sha method returns the correct digest string
        """
        username = 'foo'
        password = 'bar'
        expected = '4fa0d6984df3b91af1f0942b7522987783050b90'
        self.assertEqual(afraid.get_sha(username, password), expected)

    def test_parse_ascii_api(self):
        records = afraid.parse_ascii_api(API_OUTPUT)
        self.assertEqual(records, SAMPLE_RECORDS)

    def test_get_records_by_desc(self):
        desc = 'example.org'
        record = afraid.get_record_by_desc(SAMPLE_RECORDS, desc)
        self.assertEqual(record, SAMPLE_RECORDS[0])

    @patch('urllib2.urlopen')
    def test_update_url(self, mockurlopen):
        mockurlopen.return_value.read.return_value = ""
        afraid.update_url(SAMPLE_RECORDS[0])


API_OUTPUT = \
"""
example.org|1.1.1.1|http://freedns.afraid.org/dynamic/update.php?someFakeHash
deathstar.example.org|2.2.2.2|http://freedns.afraid.org/dynamic/update.php?eLKJDUasdfialsdDDF
eve.example.org|3.3.3.3|http://freedns.afraid.org/dynamic/update.php?eFMybzR5Vn
"""

SAMPLE_RECORDS =  [{'desc': 'example.org',
                   'ip': '1.1.1.1',
                   'url': 'http://freedns.afraid.org/dynamic/update.php?someFakeHash'},
                  {'desc': 'deathstar.example.org',
                   'ip': '2.2.2.2',
                   'url': 'http://freedns.afraid.org/dynamic/update.php?eLKJDUasdfialsdDDF'},
                  {'desc': 'eve.example.org',
                   'ip': '3.3.3.3',
                   'url': 'http://freedns.afraid.org/dynamic/update.php?eFMybzR5Vn'}]
