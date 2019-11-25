#! python

import argparse
import base64
import requests
import datacite.config

argparser = argparse.ArgumentParser(description="Query a DOI")
datacite.config.add_cli_arguments(argparser, login=False)
argparser.add_argument('doi', help="the DOI to search")
args = argparser.parse_args()
config = datacite.config.get_config(args)

headers = {'accept': 'application/vnd.api+json'}
response = requests.get(config.apiurl+args.doi, headers=headers)
if response.status_code != requests.codes.ok:
    response.raise_for_status()
doi_data = response.json()
xml = base64.b64decode(doi_data['data']['attributes']['xml'], validate=True)

print(xml.decode('utf8'))
