"""Provide the doi class, representing a DataCite doi.
"""

import base64
import json
import re
import requests

class Doi:

    DOI_re = re.compile(r"^(?:doi:)?(10\..+/.+)$")

    def __init__(self, doi):
        m = self.DOI_re.match(doi)
        if m:
            self._doi = m.group(1)
        else:
            raise ValueError("Invalid DOI '%s'" % doi)
        self._data = None

    def _init_data(self):
        self._data = {
            'data': {
                'type': 'dois',
                'attributes': {
                    'doi': self.doi,
                },
            },
        }

    @property
    def doi(self):
        return self._doi

    @property
    def attributes(self):
        if self._data is None:
            self._init_data()
        return self._data['data']['attributes']

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
        if value:
            self._data['data']['attributes']['url'] = value
        else:
            try:
                del self._data['data']['attributes']['url']
            except KeyError:
                pass

    @property
    def metadata(self):
        try:
            encoded_xml = self._data['data']['attributes']['xml']
        except (TypeError, KeyError):
            return None
        return base64.b64decode(encoded_xml, validate=True).decode('utf8')

    @metadata.setter
    def metadata(self, xml):
        if self._data is None:
            self._init_data()
        if xml:
            encoded_xml = base64.b64encode(bytes(xml)).decode('ascii')
            self._data['data']['attributes']['xml'] = encoded_xml
        else:
            try:
                del self._data['data']['attributes']['xml']
            except KeyError:
                pass

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
