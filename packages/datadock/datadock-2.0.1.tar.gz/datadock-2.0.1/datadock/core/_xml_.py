"""
Module: _xml_.py
=========================
Parses an XML document from a string containing XML content or a text file containing XML content.

### Parameters:
- doc_xml_or_txt (str): A string containing XML content or a path to a text file containing XML content.
  The XML content should be enclosed within `<XML></XML>` tags.

### Returns:
- etree._Element: The root element of the parsed XML document.

### Raises:
- ValueError: If the input does not contain valid XML content, i.e., if the input does not match the expected XML format or is missing the required `<XML></XML>` wrapper.

### Example:
```python
xml_root = parse_xml("<XML><root><child>data</child></root></XML>")
"""
import re

from lxml import etree


# Define namespaces
xml_namespaces = {
    "ns": "http://www.sec.gov/edgar/thirteenffiler",
    "com": "http://www.sec.gov/edgar/common",
}


def parse_xml(doc_xml_or_txt: str) -> etree.Element:
    """
    Parses an XML document from a string containing XML content or a text file containing XML content.

    Parameters:
    doc_xml_or_txt (str): A string containing XML content or a path to a text file containing XML content.

    Returns:
    etree._Element: The root element of the parsed XML document.

    Raises:
    ValueError: If the input does not contain valid XML content.
    """
    match = re.search(r"<XML>(.*?)</XML>", doc_xml_or_txt, re.DOTALL)
    if not match:
        raise ValueError("Valid XML content not found in the input.")

    xml_text = match.group(1).strip()

    # Convert the XML text to bytes
    xml_bytes = xml_text.encode("utf-8")  # Ensure it is encoded as bytes

    # Parse the XML
    root = etree.fromstring(xml_bytes)
    return root
