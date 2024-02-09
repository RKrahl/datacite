#! python

import argparse
import logging
from pathlib import Path
import sys
from lxml.etree import DocumentInvalid
import datacite.xml

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")
log = logging.getLogger(__name__)

argparser = argparse.ArgumentParser()
argparser.add_argument('metadata',
                       help="XML file with DOI metadata",
                       metavar="metadata.xml",
                       type=Path)
args = argparser.parse_args()

try:
    metadata = datacite.xml.XML(args.metadata)
except DocumentInvalid as exc:
    print("%s: %s" % (args.metadata, exc), file=sys.stderr)
    sys.exit(2)
