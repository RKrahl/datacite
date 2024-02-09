"""Provide the XML class.
"""

from lxml import etree


class XML:
    """A DataCite Schema XML document.

    This class provides limited access to individual properties to the
    extent of what is actually used in this package.
    """

    xml_ns = 'http://datacite.org/schema/kernel-4'
    """The URL to use for the XML name space."""
    xml_schema_url = 'http://schema.datacite.org/meta/kernel-4.5/metadata.xsd'
    """The URL of the DataCite metadata XML Schema Definition."""
    _xml_schema = None

    @classmethod
    def XMLSchema(cls):
        if not cls._xml_schema:
            cls._xml_schema = etree.XMLSchema(etree.parse(cls.xml_schema_url))
        return cls._xml_schema

    def __init__(self, path):
        with path.open('rb') as f:
            self._etree = etree.parse(f)
        self.XMLSchema().assertValid(self._etree)

    @property
    def doi(self):
        identifier = self._etree.find(".//{%s}identifier" % self.xml_ns)
        return identifier.text.strip()

    @doi.setter
    def doi(self, doi):
        identifier = self._etree.find(".//{%s}identifier" % self.xml_ns)
        for c in identifier.xpath('./comment()'):
            identifier.remove(c)
        identifier.text = doi

    @property
    def title(self):
        title = self._etree.find(".//{%s}title" % self.xml_ns)
        return title.text.strip()

    def __bytes__(self):
        return etree.tostring(self._etree,
                              encoding='UTF-8',
                              xml_declaration=True,
                              pretty_print=True)

    def __str__(self):
        return bytes(self).decode('UTF-8')
