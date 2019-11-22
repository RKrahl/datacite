#! python

import argparse
import base64
import json
from pathlib import Path
from lxml import etree
import requests
import datacite.config

argparser = argparse.ArgumentParser(description="Mint a DOI")
datacite.config.add_cli_arguments(argparser)
argparser.add_argument('doi', help="the DOI to create")
argparser.add_argument('url', help="URL of the landing page")
argparser.add_argument('metadata',
                       help="DOI metadata as DataCite XML",
                       metavar="metadata.xml",
                       type=Path)
args = argparser.parse_args()
config = datacite.config.get_config(args)

schema = etree.XMLSchema(etree.parse(datacite.config.xml_schema))
with args.metadata.open('rb') as f:
    metadata = etree.parse(f)
if not schema.validate(metadata):
    raise RuntimeError("Invalid metadata in %s." % args.metadata)

metadata_str = etree.tostring(metadata,
                              encoding='UTF-8',
                              xml_declaration=True,
                              pretty_print=True)
data = {
    'data': {
        'id': args.doi,
        'type': 'dois',
        'attributes': {
            'event': 'publish',
            'doi': args.doi,
            'url': datacite.config.xml_ns,
            'landingPage': {
                'url': args.url,
            },
            'xml': base64.b64encode(metadata_str).decode('ascii'),
        },
    },
}

headers = {'content-type': 'application/vnd.api+json'}
response = requests.post(config.url, data=json.dumps(data), headers=headers)
if response.status_code != requests.codes.ok:
    response.raise_for_status()
