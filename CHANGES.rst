Changelog
=========


0.3 (not yet released)
~~~~~~~~~~~~~~~~~~~~~~

New features
------------

+ `#3`_, `#12`_: Add support for DOIs in Draft or Registered state.

+ `#8`_, `#9`_: Add an `overview` option to `datacite-doi get`.

Incompatible changes
--------------------

+ `#13`_, `#14`_: Drop support for Python 3.10 and older.

+ `#6`_, `#7`_: Remove subcommand `bulk-create` from `datacite-doi`
  script.

Bug fixes and minor changes
---------------------------

+ `#4`_, `#5`_: Update the XML schema url for DataCite metadata to
  version 4.7.

+ `#10`_, `#11`_: `Doi.create()` should verify that the DOI attributes
  are set.

.. _#3: https://github.com/RKrahl/datacite/issues/3
.. _#4: https://github.com/RKrahl/datacite/issues/4
.. _#5: https://github.com/RKrahl/datacite/pull/5
.. _#6: https://github.com/RKrahl/datacite/issues/6
.. _#7: https://github.com/RKrahl/datacite/pull/7
.. _#8: https://github.com/RKrahl/datacite/issues/8
.. _#9: https://github.com/RKrahl/datacite/pull/9
.. _#10: https://github.com/RKrahl/datacite/issues/10
.. _#11: https://github.com/RKrahl/datacite/pull/11
.. _#12: https://github.com/RKrahl/datacite/pull/12
.. _#13: https://github.com/RKrahl/datacite/issues/13
.. _#14: https://github.com/RKrahl/datacite/pull/14


0.2 (2025-06-02)
~~~~~~~~~~~~~~~~

+ `#1`_: Add support for retrieving the DataCite API password from the
  system keyring.

+ `#2`_: Add :ref:`datacite-validate-xml` command line script.
  :class:`datacite.xml.XML` raises :exc:`lxml.etree.DocumentInvalid`
  instead of :exc:`ValueError` if the metadata fails to validate.

+ Update the XML schema url for DataCite metadata to version 4.6.

.. _#1: https://github.com/RKrahl/datacite/pull/1
.. _#2: https://github.com/RKrahl/datacite/pull/2


0.1 (2022-11-25)
~~~~~~~~~~~~~~~~

Initial public release.
