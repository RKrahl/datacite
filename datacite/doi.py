"""Provide the doi class, representing a DataCite doi.
"""

import base64
import json
from lxml import etree
import requests

class Doi:

    def __init__(self, doi):
        self._doi = doi
        self._data = None

    def _init_data(self):
        self._data = {
            'data': {
                'type': 'dois',
                'attributes': {
                    'event': None,
                    'doi': self.doi,
                    'url': None,
                    'xml': None,
                },
            },
        }

    @property
    def doi(self):
        return self._doi

    @property
    def url(self):
        try:
            return self._data['data']['attributes']['url']
        except (TypeError, KeyError):
            return None

    @url.setter
    def url(self, value):
        if self._data is None:
            self._init_data()
        self._data['data']['attributes']['url'] = value

    @property
    def metadata(self):
        try:
            xml_attr = self._data['data']['attributes']['xml']
        except (TypeError, KeyError):
            return None
        return base64.b64decode(xml_attr, validate=True).decode('utf8')

    @metadata.setter
    def metadata(self, xml):
        if hasattr(xml, "docinfo"):
            xml = etree.tostring(xml,
                                 encoding='UTF-8',
                                 xml_declaration=True,
                                 pretty_print=True)
        if self._data is None:
            self._init_data()
        xml_attr = base64.b64encode(xml).decode('ascii')
        self._data['data']['attributes']['xml'] = xml_attr

    def fetch(self, config):
        headers = {'accept': 'application/vnd.api+json'}
        response = requests.get(config.apiurl+self.doi, headers=headers)
        if response.status_code != requests.codes.ok:
            response.raise_for_status()
        self._data = response.json()

    def create(self, config, event='publish'):
        if self._data is None:
            self._init_data()
        self._data['data']['attributes']['event'] = event
        headers = {'content-type': 'application/vnd.api+json'}
        response = requests.post(config.apiurl,
                                 data=json.dumps(self._data),
                                 auth=(config.username, config.password),
                                 headers=headers)
        if response.status_code != requests.codes.ok:
            response.raise_for_status()

    def update(self, config, event='publish'):
        if self._data is None:
            raise ValueError("DOI attributes not set")
        self._data['data']['attributes']['event'] = event
        headers = {'content-type': 'application/vnd.api+json'}
        response = requests.put(config.apiurl+self.doi,
                                data=json.dumps(self._data),
                                auth=(config.username, config.password),
                                headers=headers)
        if response.status_code != requests.codes.ok:
            response.raise_for_status()
