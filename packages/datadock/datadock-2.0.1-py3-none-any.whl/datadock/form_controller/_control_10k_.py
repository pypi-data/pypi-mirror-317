"""
Module: _control_10k_.py
==========================
This class is responsible for parsing a 10-K financial report text document and extracting
relevant sections. It processes the text of the 10-K report to identify specific sections
and organizes the extracted content in a structured format suitable for further analysis.

Attributes:
- _txt_document (str): The text content of the 10-K financial report to be parsed.

Methods:
- _parse_txt_(): Parses the 10-K document text to extract sections and returns them as a PyArrow Table.

The class is a specific implementation of a form strategy designed for the 10-K financial
report. It identifies section titles, extracts corresponding content, and returns a structured
representation of the document for further processing.
"""

import re

import pyarrow as pa

from datadock.src.utils import clean_text

from datadock.factory.patterns import section_pattern_10k
from datadock.factory.formfactory import FormStrategy, to_table


class Form10KController(FormStrategy):
    """
    This class is responsible for parsing a 10-K financial report text document and extracting relevant sections.

    Attributes:
    _txt_document (str): The text content of the 10-K financial report.

    Methods:
    _parse_txt_(): Parses the text document and extracts sections into a PyArrow Table.
    """
    def _parse_txt_(self) -> pa.Table:
        """
        Parses the text document and extracts sections into a PyArrow Table.

        The function first trims the text at the position of "SIGNATURES" or "SIGNATURE" if present.
        It then initializes a list to store tuples of (section title, content).
        Next, it finds all matches for the section titles using a predefined pattern.
        For each match, it captures the start and end of the section, extracts the content, and appends it to the sections list.
        Finally, it returns the sections as a PyArrow Table.

        Returns:
        pa.Table: A PyArrow Table containing the extracted sections.
        """
        document_text = self._txt_document

        # Find the position of "SIGNATURES" or "SIGNATURE" in the document, if present
        signature_match = re.search(r"\bSIGNATURE|SIGNATURES|SIGNATUREPursuant?\b", document_text)
        if signature_match:
            document_text = document_text[: signature_match.start()]  # Trim text at the "SIGNATURES" or "SIGNATURE" position

        # Initialize a list to store tuples of (section title, content)
        sections = []

        # Find all matches for the section titles
        matches = list(section_pattern_10k.finditer(document_text))

        # Iterate over matches and extract content for each section
        for i, match in enumerate(matches):
            # Capture the start and end of each section based on the matches
            start = match.end()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(document_text)

            # Get the section title and clean it up
            section_title = match.group(0).strip()

            # Capture the content for the current section by slicing the document text
            section_content = document_text[start:end].strip()

            # Append the result as a tuple to the sections list
            sections.append((clean_text(f"{section_title}"), clean_text(section_content)))

        return to_table(sections)
