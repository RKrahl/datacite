#! python

import argparse
from pathlib import Path
from lxml import etree
import datacite.config
from datacite.doi import Doi

argparser = argparse.ArgumentParser(description="Mint a DOI")
datacite.config.add_cli_arguments(argparser)
argparser.add_argument('doi', help="the DOI to create")
argparser.add_argument('url', help="URL of the landing page")
argparser.add_argument('metadata',
                       help="XML file with DOI metadata",
                       metavar="metadata.xml",
                       type=Path)
args = argparser.parse_args()
config = datacite.config.get_config(args)

with args.metadata.open('rb') as f:
    metadata = etree.parse(f)
schema = etree.XMLSchema(etree.parse(datacite.config.xml_schema))
if not schema.validate(metadata):
    raise RuntimeError("Invalid metadata in %s." % args.metadata)

doi = Doi(args.doi)
doi.url = args.url
doi.metadata = metadata
doi.create(config)
