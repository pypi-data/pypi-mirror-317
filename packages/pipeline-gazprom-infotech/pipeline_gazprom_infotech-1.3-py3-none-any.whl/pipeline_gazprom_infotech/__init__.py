"""Base Infotech XML stuff."""
from lxml import etree as ET


def it_date(dtime):
    """Return string date in Infotech format for given datetime value."""
    return "{:02d}.{:02d}.{}".format(dtime.day, dtime.month, dtime.year)


class InfotechError(Exception):
    """Infotech exceptions."""


class InfotechBase:
    """Abstract base Infotech XML class."""

    root = None
    typobjs = None

    def save(self, file_name, encoding="windows-1251"):
        """Save XML string to file.

        Python >= 3.8
        https://stackoverflow.com/questions/62163221/creating-xml-file-with-a-specific-order-or-attributes-using-python
        """
        with open(file_name, 'wb') as out:
            out.write(ET.tostring(self.root, xml_declaration=True, encoding=encoding, pretty_print=True))

    def set_attibs(self, item, attr_dict):
        """Set attributes of given xml item."""
        for key, val in attr_dict.items():
            item.attrib[key] = val
