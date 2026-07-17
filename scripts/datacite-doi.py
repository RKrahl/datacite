#! python

import argparse
import json
import logging
from pathlib import Path
import datacite.config
from datacite.doi import State, Doi
import datacite.xml

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")
log = logging.getLogger(__name__)

argparser = argparse.ArgumentParser()
datacite.config.add_cli_arguments(argparser)
subparsers = argparser.add_subparsers(title='subcommands', dest='subcmd')


def get_metadata(args):
    config = datacite.config.get_config(args, login=args.login)
    doi = Doi(args.doi)
    doi.fetch(config)
    if args.show == 'overview':
        print("DOI: %s" % doi.doi)
        print("State: %s" % doi.state)
        print("URL: %s" % doi.url)
    elif args.show == 'metadata_xml':
        print(doi.metadata)
    elif args.show == 'attributes':
        print(json.dumps(doi.attributes, indent=2))
    else:
        raise RuntimeError("Internal error: invalid value '%s' for args.show"
                           % args.show)

get_metadata_parser = subparsers.add_parser('get', help="Query a DOI")
get_metadata_parser.add_argument('--login', action='store_true',
                                 help=("login to DataCite in order to "
                                       "search for the DOI"))
get_metadata_parser.add_argument('--show',
                                 help="select the kind of information to show",
                                 choices=['overview',
                                          'metadata_xml', 'attributes'],
                                 default='overview')
get_metadata_parser.add_argument('doi', help="the DOI to search")
get_metadata_parser.set_defaults(func=get_metadata)


def create_doi(args):
    config = datacite.config.get_config(args)
    doi = Doi(args.doi)
    if args.url:
        doi.url = args.url
    if args.metadata:
        metadata = datacite.xml.XML(args.metadata)
        metadata.doi = doi.doi
        doi.metadata = metadata
    log.info("Mint %s for %s",
             doi.doi, (metadata.title if args.metadata else "N/A"))
    doi.create(config, state=args.state)

create_parser = subparsers.add_parser('create', help="Mint a DOI")
create_parser.add_argument('--state',
                           type=State, choices=[str(s) for s in State],
                           default='findable',
                           help="create the DOI with this state")
create_parser.add_argument('--url', help="URL of the landing page")
create_parser.add_argument('--metadata',
                           help="XML file with DOI metadata",
                           metavar="metadata.xml",
                           type=Path)
create_parser.add_argument('doi', help="the DOI to create")
create_parser.set_defaults(func=create_doi)


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
    if args.state:
        need_update = True
    if need_update:
        log.info("Update %s", doi.doi)
        doi.update(config, state=args.state)
    else:
        log.info("Nothing to do")

update_parser = subparsers.add_parser('update', help="Update a DOI")
update_parser.add_argument('--state',
                           type=State, choices=[str(s) for s in State],
                           help="change the state of the DOI")
update_parser.add_argument('--url', help="URL of the landing page")
update_parser.add_argument('--metadata',
                           help="XML file with DOI metadata",
                           metavar="metadata.xml",
                           type=Path)
update_parser.add_argument('doi', help="the DOI to update")
update_parser.set_defaults(func=update_doi)


args = argparser.parse_args()
if not hasattr(args, "func"):
    argparser.error("subcommand is required")
args.func(args)
