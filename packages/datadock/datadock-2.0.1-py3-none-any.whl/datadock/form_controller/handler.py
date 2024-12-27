"""
Module: handler.py
=====================
SEC Filing Document Processing Module

This module provides tools for processing SEC filing documents in various formats (e.g., plain text, XML).
It includes functionality for parsing and extracting relevant sections from SEC forms such as SC13D and SC13G.

Key Components:
---------------
1. **doc_parsing**: A function for parsing HTML or plain text documents, cleaning them up, and returning a normalized string.
2. **FormTxtHandler**: A class that handles the parsing of SEC filing documents and returns the appropriate form controller.

Detailed Overview:
------------------
The `doc_parsing` function is used to process both HTML and plain text documents. It cleans up the text by normalizing characters, removing extra whitespace, and replacing specific characters. This is useful for ensuring that input documents are in a consistent format for further processing.

The `FormTxtHandler` class is the main controller for handling SEC filings. It determines the type of document (XML or plain text) and processes it accordingly. It also identifies the form type based on metadata and returns the corresponding form controller to handle the specific parsing logic for that form.

Module Usage:
-------------
- **doc_parsing**: Use this function to clean up and normalize input documents before further processing.
- **FormTxtHandler**: Instantiate this class with the filing information and document text to handle the SEC filing parsing process. The class will automatically detect the document type and return the appropriate form controller.

Exceptions:
-----------
- **ValueError**: Raised in `FormTxtHandler` when an unsupported form type is encountered.

Example Usage:
--------------
# Example 1: Parsing an SEC filing document
filing_info = FilingInfo(form_type="SC13G", ... )  # Create FilingInfo instance with metadata
text_doc = "Your SEC filing document text here."
handler = FormTxtHandler(filing_info=filing_info, text_doc=text_doc)
form_controller = handler.get_sections  # Get the appropriate form controller for the filing
parsed_data = form_controller._parse_txt_()  # Parse the document and get the data

# Example 2: Parsing a plain text document directly
cleaned_text = doc_parsing("Your plain text document here.")
"""

import re
import unicodedata

from lxml import html
from pydantic import BaseModel

from datadock.src.utils import restore_windows_1252_characters
from datadock.src.data_class import FilingInfo
from datadock.factory.formfactory import FormStrategy

from datadock.form_controller._control_8k_ import Form8kController
from datadock.form_controller._control_10k_ import Form10KController
from datadock.form_controller._control_sc13d_ import FormSC13DController
from datadock.form_controller._control_sc13g_ import FormSC13GController
from datadock.form_controller._control_d_ import FormDController
from datadock.form_controller._control_13fhr_ import Form13FHRController
from datadock.form_controller._control_13fnt_ import Form13FNTController


# form_types is a dictionary of all forms 8-k, 16-k, 10-k, 32-k, D etc
controllers = {
    "8-K": Form8kController,
    "10-K": Form10KController,
    "SC 13D": FormSC13DController,
    "SC 13G": FormSC13GController,
    "D": FormDController,
    "13F-HR": Form13FHRController,
    "13F-NT": Form13FNTController
}


def doc_parsing(text_doc: str) -> str:
    """
    Parses an HTML document or plain text into a clean, normalized string.

    Parameters:
    text_doc (str): The input document as a string. It can be either HTML or plain text.

    Returns:
    str: The parsed and cleaned-up text content of the document.

    This function performs the following steps:
    1. If the input is an HTML document, it extracts the text content using XPath.
    2. It normalizes the text using the NFKD Unicode normalization form.
    3. It removes newlines and multiple consecutive whitespaces.
    4. It replaces specific characters with their standard representations.
    """
    doc_tree = html.fromstring(text_doc)

    # Extract text content from the HTML document and clean up newlines/whitespace
    document_text = "".join(doc_tree.xpath("//text()"))
    document_text = restore_windows_1252_characters(unicodedata.normalize('NFKD', document_text))
    document_text = re.sub(r"\s+", " ", document_text).strip()  # Replace multiple whitespace with a single space
    document_text = (
        document_text.replace("\x92", "'")
        .replace("\x93", '"')
        .replace("\x94", '"')
        .replace("\xa0", " ")
        .replace("\u2001", " ")
    )
    return document_text


class FormTxtHandler(BaseModel):
    """
    A class to handle the parsing and processing of SEC filing documents.

    Attributes:
    filing_info (FilingInfo): Metadata information about the SEC filing.
    text_doc (str): The text content of the SEC filing document.

    Methods:
    __get_doc_type: Determines the type of the document (XML or plain text) and returns the parsed text.
    __get_sections: Identifies the form type and returns the corresponding form controller.
    get_sections: A property that calls __get_sections to retrieve the form controller.
    """

    filing_info: FilingInfo
    text_doc: str

    def __get_doc_type(self):
        """
        Determines the type of the document (XML or plain text) and returns the parsed text.

        Returns:
        str: The parsed text content of the document. If the document is XML, it returns the original XML string.
        """
        if '<XML>' in self.text_doc or '<?xml version="1.0"?>' in self.text_doc:
            return self.text_doc
        else:
            return doc_parsing(self.text_doc)

    def __get_sections(self) -> FormStrategy:
        """
        Identifies the form type and returns the corresponding form controller.

        Returns:
        FormStrategy: An instance of the form controller class corresponding to the identified form type.

        Raises:
        ValueError: If the form type is not supported.
        """
        parsed_text = self.__get_doc_type()
        form_type = self.filing_info.form_type

        for base_form in controllers:
            if form_type.startswith(base_form):
                return controllers[base_form](parsed_text)

        raise ValueError(f"Unsupported form type: {self.filing_info.form_type}")

    @property
    def get_sections(self):
        """
        A property that calls __get_sections to retrieve the form controller.

        Returns:
        FormStrategy: An instance of the form controller class corresponding to the identified form type.
        """
        return self.__get_sections()
