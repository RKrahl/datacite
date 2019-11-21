"""Create and manage DOIs using the DataCite API

This package provides scripts to mint and manage DataCite DOIs using
the DataCite API.
"""

import distutils.command.build_py
import distutils.command.sdist
import distutils.core
from distutils.core import setup
import distutils.log
from glob import glob
from pathlib import Path
import string
try:
    import setuptools_scm
    version = setuptools_scm.get_version()
    with open(".version", "wt") as f:
        f.write(version)
except (ImportError, LookupError):
    try:
        with open(".version", "rt") as f:
            version = f.read()
    except OSError:
        distutils.log.warn("warning: cannot determine version number")
        version = "UNKNOWN"

doclines = __doc__.strip().split("\n")

class sdist(distutils.command.sdist.sdist):
    def run(self):
        super().run()
        subst = {
            "version": self.distribution.get_version(),
            "url": self.distribution.get_url(),
            "description": self.distribution.get_description(),
            "long_description": self.distribution.get_long_description(),
        }
        for spec in glob("*.spec"):
            with Path(spec).open('rt') as inf:
                with Path(self.dist_dir, spec).open('wt') as outf:
                    outf.write(string.Template(inf.read()).substitute(subst))


setup(
    name = "datacite",
    version = version,
    description = doclines[0],
    long_description = "\n".join(doclines[2:]),
    author = "Rolf Krahl",
    author_email = "rolf.krahl@helmholtz-berlin.de",
    url = "https://it-ed-git.basisit.de/icat/datacite",
    license = "Internal-Use",
    requires = ["requests"],
    scripts = ["scripts/get-doi-metadata.py"],
    classifiers = [
        "Development Status :: 1 - Planning",
        "Intended Audience :: Information Technology",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    cmdclass = {'sdist': sdist},
)

