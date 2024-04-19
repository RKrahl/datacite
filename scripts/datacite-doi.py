#! python

import argparse
import json
import logging
from pathlib import Path
import yaml
import datacite.config
from datacite.doi import Doi
import datacite.xml

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")
log = logging.getLogger(__name__)

argparser = argparse.ArgumentParser()
datacite.config.add_cli_arguments(argparser)
subparsers = argparser.add_subparsers(title='subcommands', dest='subcmd')


def get_metadata(args):
    config = datacite.config.get_config(args, login=False)
    doi = Doi(args.doi)
    doi.fetch(config)
    if args.show == 'metadata_xml':
        print(doi.metadata)
    elif args.show == 'attributes':
        print(json.dumps(doi.attributes, indent=2))
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
    metadata = datacite.xml.XML(args.metadata)
    metadata.doi = doi.doi
    doi.metadata = metadata
    log.info("Mint %s for %s", doi.doi, metadata.title)
    doi.create(config)

create_parser = subparsers.add_parser('create', help="Mint a DOI")
create_parser.add_argument('doi', help="the DOI to create")
create_parser.add_argument('url', help="URL of the landing page")
create_parser.add_argument('metadata',
                           help="XML file with DOI metadata",
                           metavar="metadata.xml",
                           type=Path)
create_parser.set_defaults(func=create_doi)


def bulk_create_doi(args):
    config = datacite.config.get_config(args)
    with args.control.open('rt') as f:
        data = yaml.safe_load(f)
    count = args.doi_start_count
    for entry in data:
        try:
            if entry['ignore']:
                continue
        except KeyError:
            pass
        doi = Doi(entry['doi'] or (args.doi_format % count))
        doi.url = entry['url']
        metadata = datacite.xml.XML(Path(entry['metadata']))
        metadata.doi = doi.doi
        doi.metadata = metadata
        log.info("Mint %s for %s", doi.doi, metadata.title)
        if not args.dry_run:
            doi.create(config)
        count += 1

bulk_create_parser = subparsers.add_parser('bulk-create',
                                           help="Mint several DOIs")
bulk_create_parser.add_argument('--dry-run',
                                help=("show what would be done, "
                                      "do not actually create any DOIs"),
                                action='store_true')
bulk_create_parser.add_argument('--doi-format',
                                help=("DOI format string"),
                                default='10.5442/NI%06d')
bulk_create_parser.add_argument('--doi-start-count',
                                help=("start value for the serial number in "
                                      "the DOI"),
                                type=int, default=1)
bulk_create_parser.add_argument('control',
                                help="control file",
                                metavar="control.yaml",
                                type=Path)
bulk_create_parser.set_defaults(func=bulk_create_doi)


def update_doi(args):
    config = datacite.config.get_config(args)
    doi = Doi(args.doi)
    need_update = False
    if args.url:
        doi.url = args.url
        need_update = True
    if args.metadata:
        metadata = datacite.xml.XML(args.metadata)
        metadata.doi = doi.doi
        doi.metadata = metadata
        need_update = True
    if need_update:
        log.info("Update %s", doi.doi)
        doi.update(config)
    else:
        log.info("Nothing to do")

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
