#! python

import argparse
from pathlib import Path
import pprint
from lxml import etree
import yaml
import datacite.config
from datacite.doi import Doi

argparser = argparse.ArgumentParser()
datacite.config.add_cli_arguments(argparser)
subparsers = argparser.add_subparsers(title='subcommands', dest='subcmd')


def read_datacite_xml(path):
    with path.open('rb') as f:
        metadata = etree.parse(f)
    schema = etree.XMLSchema(etree.parse(datacite.config.xml_schema))
    if not schema.validate(metadata):
        raise RuntimeError("Invalid metadata in %s." % args.metadata)
    return metadata


def get_metadata(args):
    config = datacite.config.get_config(args, login=False)
    doi = Doi(args.doi)
    doi.fetch(config)
    if args.show == 'metadata_xml':
        print(doi.metadata)
    elif args.show == 'attributes':
        pprint.pprint(doi.attributes)
    else:
        raise RuntimeError("Internal error: invalid value '%s' for args.show"
                           % args.show)

get_metadata_parser = subparsers.add_parser('get', help="Query a DOI")
get_metadata_parser.add_argument('--show',
                                 help="select the kind of information to show",
                                 choices=['metadata_xml', 'attributes'],
                                 default='metadata_xml')
get_metadata_parser.add_argument('doi', help="the DOI to search")
get_metadata_parser.set_defaults(func=get_metadata)


def create_doi(args):
    config = datacite.config.get_config(args)
    doi = Doi(args.doi)
    doi.url = args.url
    doi.metadata = read_datacite_xml(args.metadata)
    doi.create(config)

create_parser = subparsers.add_parser('create', help="Mint a DOI")
create_parser.add_argument('doi', help="the DOI to create")
create_parser.add_argument('url', help="URL of the landing page")
create_parser.add_argument('metadata',
                           help="XML file with DOI metadata",
                           metavar="metadata.xml",
                           type=Path)
create_parser.set_defaults(func=create_doi)


def builk_create_doi(args):
    config = datacite.config.get_config(args)
    with args.control.open('rt') as f:
        data = yaml.safe_load(f)
    for entry in data:
        doi = Doi(entry['doi'])
        doi.url = entry['url']
        doi.metadata = read_datacite_xml(Path(entry['metadata']))
        doi.create(config)

builk_create_parser = subparsers.add_parser('bulk-create',
                                            help="Mint several DOIs")
builk_create_parser.add_argument('control',
                                 help="control file",
                                 metavar="control.yaml",
                                 type=Path)
builk_create_parser.set_defaults(func=builk_create_doi)


def update_doi(args):
    config = datacite.config.get_config(args)
    doi = Doi(args.doi)
    need_update = False
    if args.url:
        doi.url = args.url
        need_update = True
    if args.metadata:
        doi.metadata = read_datacite_xml(args.metadata)
        need_update = True
    if need_update:
        doi.update(config)
    else:
        print("Nothing to do")

update_parser = subparsers.add_parser('update', help="Update a DOI")
update_parser.add_argument('--url', help="URL of the landing page")
update_parser.add_argument('--metadata',
                           help="XML file with DOI metadata",
                           metavar="metadata.xml",
                           type=Path)
update_parser.add_argument('doi', help="the DOI to create")
update_parser.set_defaults(func=update_doi)


args = argparser.parse_args()
if not hasattr(args, "func"):
    argparser.error("subcommand is required")
args.func(args)
