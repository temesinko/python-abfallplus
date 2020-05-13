# -*- coding: utf-8 -*-

"""A library providing a Python interface to the Abfall+ API"""

from .models import (
    Community,
    Street,
    WasteType,
)
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import logging
import requests

logger = logging.getLogger(__name__)


class Api(object):
    """A Python interface to the Abfall+ API"""

    BASE_URL_WEBSITE = 'https://www.abfallplus.de'
    BASE_URL_API = 'https://api.abfall.io'
    MODE_COMPANY_WIDGET = 'd6c5855a62cf32a4dadbc2831f0f295f'
    DEFAULT_HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/81.0.4044.138 Safari/537.36'
    }

    def __init__(self):
        """Instantiate a new abfallplus.Api object."""

    def get_communities(self,
                        company_key):
        """Return all communities covered by the waste management company behind the defined key

        Args:
            company_key (str):
                Key of the waste management company
        Returns:
            list: A sequence of abfallplus.Community instances.
        """

        url = '%s/' % self.BASE_URL_API
        params = {
            'key': company_key,
            'modus': self.MODE_COMPANY_WIDGET,
            'waction': 'init'
        }

        resp = requests.get(url, params, headers=self.DEFAULT_HEADERS)
        soup = BeautifulSoup(resp.text, 'html.parser')
        communities = []

        for option in soup.find_all('option'):
            # Skip default select option
            if option['value'] == '0':
                continue
            communities.append(Community(id=int(option['value']), title=option.string))

        return communities

    def get_streets(self,
                    company_key,
                    community_id):
        """Return all streets in the defined community covered by the waste management company behind the defined key

        Args:
            company_key (str):
                Key of the waste management company
            community_id (id):
                ID of the community
        Returns:
            list: A sequence of abfallplus.Street instances.
        """

        url = '%s/' % self.BASE_URL_API
        params = {
            'key': company_key,
            'modus': self.MODE_COMPANY_WIDGET,
            'waction': 'auswahl_kommune_set'
        }

        resp = requests.post(url, {'f_id_kommune': community_id}, params=params, headers=self.DEFAULT_HEADERS)
        soup = BeautifulSoup(resp.text, 'html.parser')
        streets = []

        for option in soup.find_all('option'):
            # Skip default select option
            if option['value'] == '0':
                continue
            streets.append(Street(id=int(option['value']), title=option.string))

        return streets

    def get_waste_types(self,
                        company_key,
                        street_id):
        """Return all waste types in the specified street covered by the waste management company behind the defined key

        Args:
            company_key (str):
                Key of the waste management company
            street_id (int):
                ID of the street
        Returns:
            list: A sequence of abfallplus.WasteType instances.
        """

        url = '%s/' % self.BASE_URL_API
        params = {
            'key': company_key,
            'modus': self.MODE_COMPANY_WIDGET,
            'waction': 'auswahl_strasse_set'
        }

        data = {
            'f_id_strasse': street_id,
        }

        resp = requests.post(url, data, params=params, headers=self.DEFAULT_HEADERS)
        soup = BeautifulSoup(resp.text, 'html.parser')
        waste_types = []

        for row in soup.find_all('div', {'class': 'awk-ui-input-tr'}):
            # Skip unwanted inputs
            lbl = row.find('label')
            inp = row.find('input')
            if lbl is None or inp is None:
                continue
            spans = lbl.find_all('span', {'class': 'awk-ui-offscreen'})
            for span in spans:
                span.extract()
            waste_types.append(WasteType(id=int(inp['value']), title=lbl.text))

        return waste_types

    def get_waste_collection_dates(self,
                                   company_key,
                                   street_id,
                                   date_from,
                                   date_to,
                                   waste_types=None):
        """Return collection dates for the defined street in the defined period of time using the given company key.
        You can also filter for specific waste types.

        Args:
            company_key (str):
                Key of the waste management company.
            street_id (int):
                ID of the street.
            date_from (datetime)
                Start date.
            date_to (datetime)
                End date.
            waste_types (list, optional)
                List of waste type IDs to fetch. Defaults to empty list and therefore all types are fetched.
        Returns:
            dict: A dictionary containing the waste types as keys and collection dates as values.
        """

        if waste_types is None:
            waste_types = []
        url = '%s/' % self.BASE_URL_API
        params = {
            'key': company_key,
            'modus': self.MODE_COMPANY_WIDGET,
            'waction': 'export_csv'
        }

        data = {
            'f_id_strasse': street_id,
            'f_abfallarten': ','.join([str(i) for i in waste_types]),
            'f_zeitraum': '{}-{}'.format(date_from.strftime("%Y%m%d"), date_to.strftime("%Y%m%d"))
        }

        resp = requests.post(url, data, params=params, headers=self.DEFAULT_HEADERS)
        waste_collection_dates = {}

        reader = csv.reader(resp.text.splitlines(), delimiter=';')
        line_count = 0
        keys = []
        for row in reader:
            col_idx = 0
            if line_count == 0:
                for column in row:
                    waste_collection_dates[column] = []
                    keys.append(column)
            else:
                for column in row:
                    if not column:
                        continue
                    waste_collection_dates[keys[col_idx]].append(column)
                    col_idx += 1
            line_count += 1

        return waste_collection_dates
