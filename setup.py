"""Create and manage DOIs using the DataCite API

This package provides a command line script to mint and manage
DataCite DOIs using the DataCite REST API.
"""

import setuptools
from setuptools import setup
import setuptools.command.build_py
import distutils.command.sdist
import distutils.dist
from distutils import log
from glob import glob
from pathlib import Path
import string
try:
    import gitprops
    release = gitprops.get_last_release()
    release = release and str(release)
    version = str(gitprops.get_version())
except (ImportError, LookupError):
    try:
        from _meta import release, version
    except ImportError:
        log.warn("warning: cannot determine version number")
        release = version = "UNKNOWN"

docstring = __doc__


# Enforcing of PEP 625 has been added in setuptools 69.3.0.  We don't
# want this, we want to keep control on the name of the sdist
# ourselves.  Disable it.
def _fixed_get_fullname(self):
    return "%s-%s" % (self.get_name(), self.get_version())

distutils.dist.DistributionMetadata.get_fullname = _fixed_get_fullname


class meta(setuptools.Command):

    description = "generate meta files"
    user_options = []
    meta_template = '''
release = %(release)r
version = %(version)r
'''

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        version = self.distribution.get_version()
        log.info("version: %s", version)
        values = {
            'release': release,
            'version': version,
        }
        with Path("_meta.py").open("wt") as f:
            print(self.meta_template % values, file=f)


# Note: Do not use setuptools for making the source distribution,
# rather use the good old distutils instead.
# Rationale: https://rhodesmill.org/brandon/2009/eby-magic/
class sdist(distutils.command.sdist.sdist):
    def run(self):
        self.run_command('meta')
        super().run()
        subst = {
            "version": self.distribution.get_version(),
            "url": self.distribution.get_url(),
            "description": docstring.split("\n")[0],
            "long_description": docstring.split("\n", maxsplit=2)[2].strip(),
        }
        for spec in glob("*.spec"):
            with Path(spec).open('rt') as inf:
                with Path(self.dist_dir, spec).open('wt') as outf:
                    outf.write(string.Template(inf.read()).substitute(subst))


class build_py(setuptools.command.build_py.build_py):
    def run(self):
        self.run_command('meta')
        super().run()
        package = self.distribution.packages[0].split('.')
        outfile = self.get_module_outfile(self.build_lib, package, "_meta")
        self.copy_file("_meta.py", outfile, preserve_mode=0)


with Path("README.rst").open("rt", encoding="utf8") as f:
    readme = f.read()

setup(
    name = "datacite",
    version = version,
    description = docstring.split("\n")[0],
    long_description = readme,
    url = "https://github.com/RKrahl/datacite",
    author = "Rolf Krahl",
    author_email = "rolf.krahl@helmholtz-berlin.de",
    license = "Apache-2.0",
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Programming Language :: Python :: 3.15",
    ],
    packages = ["datacite"],
    package_dir = {"": "src"},
    scripts = [
        "src/scripts/datacite-doi.py",
        "src/scripts/datacite-validate-xml.py",
    ],
    python_requires = ">=3.11",
    install_requires = ["setuptools", "keyring", "lxml", "requests"],
    cmdclass = dict(build_py=build_py, sdist=sdist, meta=meta),
)
