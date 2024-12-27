"""
Module: _control_sc13g_.py
============================
This class is responsible for parsing a SC13G filing document and extracting specific sections,
such as Items 1 to 3 and Items 4 to 10, based on predefined patterns. The SC13G form is used
to report beneficial ownership of securities. This class processes the document and organizes
the extracted sections into a structured format.

Attributes:
- _txt_document (str): The text content of the SC13G filing document to be parsed.

Methods:
- _parse_txt_(): Parses the SC13G document text, extracts relevant sections (Item 1 to Item 3,
  and Item 4 to Item 10), and returns the extracted data as a PyArrow Table.
- _get_item1_to_item3(): Extracts sections corresponding to Items 1, 2, and 3 from the document.
- _get_item4_to_item10(): Extracts sections corresponding to Items 4 through 10 from the document.
- _extract_items(): Extracts and structures the content for Items 1 to 3 based on predefined patterns.

The class provides a strategy for handling SC13G filings and allows for efficient parsing
and extraction of critical information from the document for further processing and analysis.
"""

import re
from typing import List, Tuple

import pyarrow as pa

from datadock.src.utils import clean_text

from datadock.factory.formfactory import FormStrategy, to_table

from datadock.factory.patterns import section_pattern_13g_1, section_pattern_13g_2


class FormSC13GController(FormStrategy):
    def _parse_txt_(self) -> pa.Table:
        """
        Parses the text document and extracts relevant sections for Form SC 13G.

        Parameters:
        - self._txt_document (str): The text content of the document to be parsed.

        Returns:
        - pa.Table: A PyArrow table containing the extracted data.
        """
        document_text = self._txt_document

        item1_to_3 = self._extract_items(self._get_item1_to_item3(document_text))
        item4_to_10 = self._get_item4_to_item10(document_text)

        combined_lists = item1_to_3 + item4_to_10

        return to_table(combined_lists)

    @staticmethod
    def _get_item1_to_item3(text_doc: str) -> List[Tuple[str, str]]:
        """
        Extracts sections from Item 1 to Item 3 from the given text document.

        Parameters:
        - text_doc (str): The text content of the document.

        Returns:
        - List[Tuple[str, str]]: A list of tuples, where each tuple contains the section title and content.
        """
        # Find the position of "Item 4" in the document, if present
        item4_match = re.search(r'\b[Ii][Tt][Ee][Mm]\s*4(?:[\.\)]|\s)(Ownership)?(?:[\.\)]|\s|$)', text_doc, re.IGNORECASE)
        if item4_match:
            text_doc = text_doc[:item4_match.start()]  # Trim text at the "Item 4" position

        # Initialize a list to store tuples of (section title, content)
        sections = []

        # Find all matches for the section titles
        matches = list(section_pattern_13g_1.finditer(text_doc))
        # Iterate over matches and extract content for each section
        for i, match in enumerate(matches):
            # Capture the start and end of each section based on the matches
            start = match.end()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(text_doc)

            # Get the section title and clean it up
            section_title = match.group(0).strip()

            # Capture the content for the current section by slicing the document text
            section_content = text_doc[start:end].strip()

            # Append the result as a tuple to the sections list
            sections.append((clean_text(section_title), clean_text(section_content)))

        pattern = re.compile(r"Item\s*1\s*[\.\s]*\(?a\)?[\.\s]*Name\s*of\s*Issuer", re.IGNORECASE)

        for index, (title, _) in enumerate(sections):
            if pattern.match(title):
                # Return the list starting from the found index
                return sections[index:]

        return sections

    @staticmethod
    def _get_item4_to_item10(text_doc: str) -> List[Tuple[str, str]]:
        """
        Extracts sections from Item 4 to Item 10 from the given text document.

        Parameters:
        - text_doc (str): The text content of the document.

        Returns:
        - List[Tuple[str, str]]: A list of tuples, where each tuple contains the section title and content.
        """
        # Find the position of "SIGNATURES" or "SIGNATURE" in the document, if present
        signature_match = re.search(r'\bSIGNATURE|SIGNATURES|SIGNATUREPursuant?\b', text_doc, re.IGNORECASE)
        if signature_match:
            text_doc = text_doc[:signature_match.start()]  # Trim text at the "SIGNATURES" or "SIGNATURE" position

        # Initialize a list to store tuples of (section title, content)
        sections = []

        # Find all matches for the section titles
        matches = list(section_pattern_13g_2.finditer(text_doc))
        # Iterate over matches and extract content for each section
        for i, match in enumerate(matches):
            # Capture the start and end of each section based on the matches
            start = match.end()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(text_doc)

            # Get the section title and clean it up
            section_title = match.group(0).strip()

            # Capture the content for the current section by slicing the document text
            section_content = text_doc[start:end].strip()

            # Append the result as a tuple to the sections list
            sections.append((clean_text(section_title), clean_text(section_content)))

        return sections

    @staticmethod
    def _extract_items(data: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
        """
        Extracts specific items (Item 1, Item 2, and Item 3) from the given data.

        Parameters:
        - data (List[Tuple[str, str]]): A list of tuples, where each tuple contains the section title and content.

        Returns:
        - List[Tuple[str, str]]: A list of tuples, where each tuple contains the extracted item title and content.
        """
        cleaned_data = [(item[0],) for item in data]
        result = []
        current_item = None

        for entry in cleaned_data:
            # Extract the string from the tuple
            text = entry[0].lower()

            # Check for Item 1, Item 2, or Item 3 in the text
            if "item 1" in text:
                if current_item != "Item 1 (a) and (b)":
                    current_item = "Item 1 (a) and (b)"
                    item_tuple = (current_item, text.split("item 1", 1)[1].strip())
                    result.append(item_tuple)
                else:
                    item_tuple = ("Item 1 (a) and (b)", text.split("item 1", 1)[1].strip())
                    result.append(item_tuple)

            elif "item 2" in text:
                if current_item != "Item 2 (a), (b), (c), (d) and (e)":
                    current_item = "Item 2 (a), (b), (c), (d) and (e)"
                    item_tuple = (current_item, text.split("item 2", 1)[1].strip())
                    result.append(item_tuple)
                else:
                    item_tuple = ("Item 2 (a), (b), (c), (d) and (e)", text.split("item 2", 1)[1].strip())
                    result.append(item_tuple)

            elif "item 3" in text:
                if current_item != "Item 3":
                    current_item = "Item 3"
                    item_tuple = (current_item, text.split("item 3", 1)[1].strip())
                    result.append(item_tuple)
                else:
                    item_tuple = ("Item 3", text.split("item 3", 1)[1].strip())
                    result.append(item_tuple)

        return result
