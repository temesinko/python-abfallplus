# -*- coding: utf-8 -*-
import unittest

import abfallplus

from datetime import datetime
import os
import sys
import responses
from responses import GET, POST

cwd = os.path.abspath(os.path.dirname(__file__))


class ErrorRedirect(object):
    """Write output to nowhere"""

    def write(self, data):
        pass


class ApiTest(unittest.TestCase):

    def setUp(self):
        self.api = abfallplus.Api()
        self._stderr = sys
        sys.stderr = ErrorRedirect()

    def tearDown(self):
        sys.stderr = self._stderr

    @staticmethod
    def read_sample_file(filename):
        with open(os.path.join(cwd, '../test_data', filename)) as f:
            return f.read()

    @responses.activate
    def test_get_communities(self):
        url = '{base_url}/?key={key}&modus={mode}&waction={action}'.format(
            base_url=self.api.BASE_URL_API,
            key='test_key',
            mode=self.api.MODE_COMPANY_WIDGET,
            action='init',
        )
        responses.add(GET, url, body=self.read_sample_file('widget_init.html'))
        resp = self.api.get_communities('test_key')
        self.assertEqual(len(resp), 192)
        self.assertTrue(type(resp[0]) is abfallplus.Community)
        self.assertEqual(resp[0].id, 2430)
        self.assertEqual(resp[0].title, 'Ailertchen')

    @responses.activate
    def test_get_streets(self):
        url = '{base_url}/?key={key}&modus={mode}&waction={action}'.format(
            base_url=self.api.BASE_URL_API,
            key='test_key',
            mode=self.api.MODE_COMPANY_WIDGET,
            action='auswahl_kommune_set',
        )
        responses.add(POST, url, body=self.read_sample_file('widget_auswahl_kommune_set.html'))
        resp = self.api.get_streets('test_key', 1234)
        self.assertEqual(len(resp), 62)
        self.assertTrue(type(resp[0]) is abfallplus.Street)
        self.assertEqual(resp[0].id, 1459)
        self.assertEqual(resp[0].title, 'Am Alten Bahnhof')

    @responses.activate
    def test_get_waste_types(self):
        url = '{base_url}/?key={key}&modus={mode}&waction={action}'.format(
            base_url=self.api.BASE_URL_API,
            key='test_key',
            mode=self.api.MODE_COMPANY_WIDGET,
            action='auswahl_strasse_set',
        )
        responses.add(POST, url, body=self.read_sample_file('widget_auswahl_strasse_set.html'))
        resp = self.api.get_waste_types('test_key', 2345)
        self.assertEqual(len(resp), 8)
        self.assertTrue(type(resp[0]) is abfallplus.WasteType)
        self.assertEqual(resp[0].id, 27)
        self.assertEqual(resp[0].title, 'Altpapier')

    @responses.activate
    def test_get_waste_collection_dates(self):
        url = '{base_url}/?key={key}&modus={mode}&waction={action}'.format(
            base_url=self.api.BASE_URL_API,
            key='test_key',
            mode=self.api.MODE_COMPANY_WIDGET,
            action='export_csv',
        )
        responses.add(POST, url, body=self.read_sample_file('widget_export_csv.csv'))
        resp = self.api.get_waste_collection_dates('test_key', 2345, datetime.now(), datetime.now())
        self.assertTrue(type(resp) is dict)
        self.assertEqual(len(resp.items()), 8)
        key_found = False
        for key in resp.keys():
            if key == 'Bioabfall':
                key_found = True
        self.assertTrue(key_found)
        self.assertEqual(len(resp['Bioabfall']), 26)
        self.assertEqual(resp['Bioabfall'][0], '07.01.2020')
