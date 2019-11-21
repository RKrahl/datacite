#! python

import argparse
import base64
import requests

url = 'https://api.datacite.org/dois/'

argparser = argparse.ArgumentParser(description="Query a DOI")
argparser.add_argument('-w', '--url',
                       help="URL of the dois API endpoint", default=url)
argparser.add_argument('doi', help="the DOI to search")
args = argparser.parse_args()

if not args.url.endswith('/'):
    args.url += '/'

headers = {'accept': 'application/vnd.api+json'}
response = requests.get(args.url+args.doi, headers=headers)
if response.status_code != requests.codes.ok:
    response.raise_for_status()
doi_data = response.json()
xml = base64.b64decode(doi_data['data']['attributes']['xml'], validate=True)

print(xml.decode('utf8'))
