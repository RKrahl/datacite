Changelog
=========


0.2 (not yet released)
~~~~~~~~~~~~~~~~~~~~~~

+ `#1`_: Add support for retrieving the DataCite API password from the
  system keyring.

+ `#2`_: Add :ref:`datacite-validate-xml` command line script.
  :class:`datacite.xml.XML` raises :exc:`lxml.etree.DocumentInvalid`
  instead of :exc:`ValueError` if the metadata fails to validate.

+ Update the XML schema url for DataCite metadata to version 4.5

.. _#1: https://github.com/RKrahl/datacite/pull/1
.. _#2: https://github.com/RKrahl/datacite/pull/2


0.1 (2022-11-25)
~~~~~~~~~~~~~~~~

Initial public release.
