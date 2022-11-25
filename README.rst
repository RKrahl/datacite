Create and manage DOIs using the DataCite API
=============================================

This package provides a command line script to mint and manage
`DataCite`_ DOIs using the `DataCite REST API`_.

I wrote this package for my own use at `Helmholtz-Zentrum Berlin für
Materialien und Energie`_.  The current development status is planning
and exploring.  Nothing here is stable yet.


System requirements
-------------------

Python:

+ Python 3.4 or newer.

Required library packages:

+ `setuptools`_
+ `lxml`_
+ `Requests`_
+ `PyYAML`_

Optional library packages:

+ `setuptools_scm`_

  The version number is managed using this package.  All source
  distributions add a static text file with the version number and
  fall back using that if `setuptools_scm` is not available.  So this
  package is only needed to build out of the plain development source
  tree as cloned from Git repository.


Copyright and License
---------------------

Copyright 2019–2022
Helmholtz-Zentrum Berlin für Materialien und Energie GmbH

Licensed under the `Apache License`_, Version 2.0 (the "License"); you
may not use this package except in compliance with the License.

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
implied.  See the License for the specific language governing
permissions and limitations under the License.


.. _DataCite: https://datacite.org/
.. _DataCite REST API: https://support.datacite.org/docs/api
.. _Helmholtz-Zentrum Berlin für Materialien und Energie: https://www.helmholtz-berlin.de/
.. _setuptools: https://github.com/pypa/setuptools/
.. _lxml: https://lxml.de/
.. _Requests: http://python-requests.org/
.. _PyYAML: https://github.com/yaml/pyyaml
.. _setuptools_scm: https://github.com/pypa/setuptools_scm/
.. _Apache License: https://www.apache.org/licenses/LICENSE-2.0
