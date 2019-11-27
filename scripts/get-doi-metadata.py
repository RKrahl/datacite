#! python

import argparse
import datacite.config
from datacite.doi import Doi

argparser = argparse.ArgumentParser(description="Query a DOI")
datacite.config.add_cli_arguments(argparser, login=False)
argparser.add_argument('doi', help="the DOI to search")
args = argparser.parse_args()
config = datacite.config.get_config(args)

doi = Doi(args.doi)
doi.fetch(config)
print(doi.metadata)
