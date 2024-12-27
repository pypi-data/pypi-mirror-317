"""
Modules: _control_8k_.py
=============================
This class is responsible for parsing and extracting sections from a 8-K filing document.
It processes the text content of the document and organizes it into structured sections
that can be further analyzed or manipulated.

Attributes:
- _txt_document (str): The text content of the 8-K filing document to be parsed.

Methods:
- _parse_txt_(): Parses the document text to extract sections, cleaning and organizing them into a PyArrow Table.

The class is a specific implementation of a form strategy, tailored to handle the parsing of
8-K filing documents. It processes the document by identifying section titles and corresponding
content, ensuring the results are returned in a structured format suitable for further analysis.
"""

import re

import pyarrow as pa

from datadock.src.utils import clean_text

from datadock.factory.patterns import section_pattern_8k
from datadock.factory.formfactory import FormStrategy, to_table


class Form8kController(FormStrategy):
    """
    This class is responsible for parsing and extracting sections from a 8-K filing document.

    Attributes:
    _txt_document (str): The text content of the 8-K filing document.

    Methods:
    _parse_txt_(): Parses the document text and extracts sections into a PyArrow Table.
    """

    def _parse_txt_(self) -> pa.Table:
        """
        Parses the document text and extracts sections into a PyArrow Table.

        The function first trims the text at the position of "SIGNATURES" or "SIGNATURE" if present.
        It then initializes a list to store tuples of (section title, content).
        Next, it finds all matches for the section titles using a predefined pattern.
        For each match, it captures the start and end of the section, extracts the content,
        cleans up the section title and content, and appends them as a tuple to the sections list.
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
        matches = list(section_pattern_8k.finditer(document_text))

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
