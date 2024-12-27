"""
Module: data_class.py
=========================
Data Classes for SEC Filing Information

This module defines data classes that represent various aspects of SEC filing documents and their associated metadata. These classes are used to structure and manage the data related to SEC filings, including details about specific filings, documents, and the state of filings.

Classes:
--------
1. **FilingsState**: Represents the state of filings for a specific page, including the starting index and total number of filings.
2. **FilingInfo**: Represents detailed information about a specific SEC filing, such as the CIK, accession number, and form type.
3. **FilingDocInfo**: Contains detailed information about a specific SEC filing document, including filing information, file number, IRS number, and SIC code.
4. **FilingTxtDoc**: Represents the raw text content of a filing document, including the document type and filing information.

Detailed Overview:
------------------
The `FilingsState` class is used to track the state of filings on a particular page. It contains the starting index (`page_start`) and the total number of filings available (`num_filings`). This class is useful for managing pagination when retrieving filings.

The `FilingInfo` class stores basic information about a specific SEC filing, such as the Central Index Key (CIK), the accession number assigned by the SEC, and optionally, the form type (e.g., 10-K, 13D, etc.).

The `FilingDocInfo` class provides detailed metadata about a filing document, including references to the associated `FilingInfo`, file number, IRS number, and Standard Industrial Classification (SIC) code.

The `FilingTxtDoc` class is used to represent the text content of a filing document. It includes the document type (e.g., 10-K, 10-Q) and the raw text of the document, along with optional filing information.

Class Usage:
-------------
- **FilingsState**: Use this class to manage and track the state of filings, including pagination when retrieving filings from the SEC database.
- **FilingInfo**: This class is helpful for organizing and representing basic metadata about SEC filings, such as CIK, accession number, and form type.
- **FilingDocInfo**: Use this class to store detailed metadata about SEC filing documents, which may include the IRS number, SIC code, and file number.
- **FilingTxtDoc**: This class can be used for managing raw text content of SEC filings and associating it with filing metadata.

Example Usage:
--------------
# Example 1: Creating and using the FilingsState class
filings_state = FilingsState(page_start=1, num_filings=100)

# Example 2: Creating FilingInfo for a specific filing
filing_info = FilingInfo(cik="0000320193", accession_number="0000320193-20-000010", form_type="10-K")

# Example 3: Storing detailed filing document information
filing_doc_info = FilingDocInfo(filing=filing_info, file_number="123456789", IRS="12-3456789", SIC="1234")

# Example 4: Storing a text document for a filing
filing_txt_doc = FilingTxtDoc(doc_type="10-K", raw_txt="This is the raw content of the document.", filing_info=filing_info)
"""

from dataclasses import dataclass, field


@dataclass
class FilingsState:
    """
    Represents the state of filings for a specific page.

    Attributes:
    ----------
    page_start : int
        The starting index of the page for the filings.
    num_filings : int
        The total number of filings available for the page.

    Methods:
    --------
    None

    """
    page_start: int
    num_filings: int


@dataclass
class FilingInfo:
    """
    Represents information about a specific SEC filing.

    Attributes:
    ----------
    cik : str
        Central Index Key (CIK) of the company associated with the filing.
    accession_number : str
        Accession number assigned by the SEC to the filing.
    form_type : str, optional
        The type of the SEC form associated with the filing. Default is an empty string.

    Methods:
    --------
    None

    """
    cik: str
    accession_number: str
    form_type: str = field(default="")


@dataclass
class FilingDocInfo:
    """
    Represents information about a specific SEC filing document.

    Attributes:
    ----------
    filing : FilingInfo
        The filing information associated with this document.
    file_number : str
        The file number assigned by the SEC to the filing.
    IRS : str
        The Internal Revenue Service (IRS) number of the company associated with the filing.
    SIC : str
        The Standard Industrial Classification (SIC) code of the company associated with the filing.
    """
    filing: FilingInfo
    file_number: str
    IRS: str
    SIC: str


@dataclass
class FilingTxtDoc:
    """
    Represents a text document associated with a specific SEC filing.

    Attributes:
    ----------
    doc_type : str
        The type of the document (e.g., 10-K, 10-Q, etc.).
    raw_txt : str
        The raw text content of the document.
    filing_info : FilingInfo, optional
        The filing information associated with this document. Default is an empty FilingInfo object.
    """
    doc_type: str
    raw_txt: str
    filing_info: FilingInfo = field(default="")
