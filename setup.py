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


class init_py(distutils.core.Command):

    description = "generate the main __init__.py file"
    user_options = []
    init_template = '''"""%s"""

__version__ = "%s"
'''

    def initialize_options(self):
        self.package_dir = None

    def finalize_options(self):
        self.package_dir = {}
        if self.distribution.package_dir:
            for name, path in self.distribution.package_dir.items():
                self.package_dir[name] = convert_path(path)

    def run(self):
        try:
            pkgname = self.distribution.packages[0]
        except IndexError:
            distutils.log.warn("warning: no package defined")
        else:
            pkgdir = Path(self.package_dir.get(pkgname, pkgname))
            ver = self.distribution.get_version()
            if not pkgdir.is_dir():
                pkgdir.mkdir()
            with (pkgdir / "__init__.py").open("wt") as f:
                print(self.init_template % (__doc__, ver), file=f)


class sdist(distutils.command.sdist.sdist):
    def run(self):
        self.run_command('init_py')
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


class build_py(distutils.command.build_py.build_py):
    def run(self):
        self.run_command('init_py')
        super().run()


setup(
    name = "datacite",
    version = version,
    description = doclines[0],
    long_description = "\n".join(doclines[2:]),
    author = "Rolf Krahl",
    author_email = "rolf.krahl@helmholtz-berlin.de",
    url = "https://it-ed-git.basisit.de/jsi/datacite",
    license = "Internal-Use",
    requires = ["lxml", "requests"],
    packages = ["datacite"],
    scripts = ["scripts/create-doi.py", "scripts/get-doi-metadata.py"],
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
    cmdclass = {'build_py': build_py, 'sdist': sdist, 'init_py': init_py},
)

