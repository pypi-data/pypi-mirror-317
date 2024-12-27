"""
Module: _control_sc13d_.py
=============================
This class is responsible for parsing a text document and extracting specific sections
from a SC13D filing. The SC13D form is used for reporting the acquisition of a significant
ownership stake in a company. This class processes the document to identify sections
defined by predefined patterns and organizes them into a structured format for further analysis.

Attributes:
- _txt_document (str): The text content of the SC13D filing to be parsed.

Methods:
- _parse_txt_(): Parses the SC13D document text to extract sections and returns them
  as a PyArrow Table.

The class is a specific implementation of a form strategy designed for SC13D filings.
It extracts sections from the filing, cleaning and organizing the data into a format
suitable for analysis.
"""

import re

import pyarrow as pa

from datadock.src.utils import clean_text

from datadock.factory.formfactory import FormStrategy, to_table

from datadock.factory.patterns import section_pattern_13d


class FormSC13DController(FormStrategy):
    """
    This class is responsible for parsing a text document and extracting specific sections.
    The document is assumed to be in the format of a SC13D form.

    Attributes:
    _txt_document (str): The text document to be parsed.

    Methods:
    _parse_txt_(): Parses the text document and extracts sections based on predefined patterns.
                   Returns a PyArrow Table containing the extracted sections.
    """

    def _parse_txt_(self) -> pa.Table:
        """
        Parses the text document and extracts sections based on predefined patterns.

        Parameters:
        None

        Returns:
        pa.Table: A PyArrow Table containing the extracted sections. Each row represents a section,
                 with columns for section title and content.
        """
        document_text = self._txt_document
        # Find the position of "SIGNATURES" or "SIGNATURE" in the document, if present
        signature_match = re.search(
            r"\bSIGNATURE|SIGNATURES|SIGNATUREPursuant?\b", document_text, re.IGNORECASE
        )
        if signature_match:
            document_text = document_text[
                : signature_match.start()
            ]  # Trim text at the "SIGNATURES" or "SIGNATURE" position

        # Initialize a list to store tuples of (section title, content)
        sections = []

        # Find all matches for the section titles
        matches = list(section_pattern_13d.finditer(document_text))

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
