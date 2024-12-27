"""
Module: utils.py
==================
This module contains various utility functions that are used across the application to
simplify common tasks, such as data manipulation, string formatting, date handling,
validation, and other helper functions.

Each function in this module is designed to encapsulate a specific task, making the codebase more modular,
reusable, and easier to maintain.

"""
import re
from typing import Dict, Optional
from bs4 import BeautifulSoup, Tag

from datadock.src.config import check_sec_identity
from datadock.src._constants import text_extensions
from datadock.src._errors import DataDockError


identity = check_sec_identity()

# Regex pattern to detect '-index' with a valid extension
index_pattern = re.compile(r"-index(?:{})$".format("|".join(re.escape(ext) for ext in text_extensions)))
r_pattern = re.compile(r"R\d+\.htm$")


def build_url(
        url_name: str = "",
        cik: str = None,
        accession_number: str = None,
        extra_path: str = "",
        path_ext: str = "",
) -> str:
    """
    Construct a URL for SEC filings using the provided parameters.

    This function constructs a URL for SEC filings by combining the provided parameters.
    It ensures that the accession number is not None and cleans it by removing any hyphens.

    Parameters:
    - url_name (str): The base URL name for the SEC filings.
    - cik (str): The Central Index Key (CIK) of the company.
    - accession_number (str): The accession number of the filing.
    - extra_path (str): Extra path components to be appended to the URL.
    - path_ext (str): The file extension to be appended to the URL.

    Returns:
    str: The constructed URL for the SEC filings.

    Raises:
    ValueError: If the accession number is None.
    """
    if accession_number is None:
        raise ValueError("Accession number is None, cannot build url")
    cleaned_accession = accession_number.replace("-", "")
    return f"{url_name}/{cik}/{cleaned_accession}/{extra_path}{path_ext}"


def make_http_headers() -> Dict[str, str]:
    """
    Make SEC HTTP Headers
    :return:
    """
    if not identity:
        raise ValueError("SEC identity not found. Call the sec_identity first")
    return {
        "User-Agent": identity,
        "Accept-Encoding": "gzip",
        "Content-Type": "application/json",
    }


def check_url_ext(url: str) -> str:
    """
    Check the file extension of a given URL.

    This function takes a URL as input and checks if it has a ".txt" extension or
    if it ends with "-index" followed by a valid file extension. The valid file extensions
    are defined in the `text_extensions` list.

    Parameters:
    - url (str): The URL to be checked.

    Returns:
    str: The file extension of the URL. If the URL has a ".txt" extension, the function
    returns "txt". If the URL ends with "-index" followed by a valid file extension, the
    function returns "index". If none of the conditions are met, the function returns an
    empty string.

    Example:
    >>> check_url_ext('https://example.com/file.txt')
    'txt'
    >>> check_url_ext('https://example.com/file-index.html')
    'index'
    >>> check_url_ext('https://example.com/file.pdf')
    ''
    """
    url = url.strip()

    # Check for ".txt" extension
    if url.endswith(".txt"):
        return "txt"

    # Check for "-index" with an extension
    if index_pattern.search(url):
        return "index"
    elif r_pattern.search(url):
        return "Rfile"


def check_link_format(link: str) -> bool:
    """
    Checks if the given link follows a specific format.

    The function uses a regular expression pattern to match links that have
    a format like 'R<digits>.htm', where <digits> represents one or more numeric
    digits. The function returns True if the link matches the format, and False otherwise.

    Parameters:
    - link (str): The link to be checked for the specified format.

    Returns:
    bool: True if the link matches the format, False otherwise.

    Example:
    >>> check_link_format('R12345.htm')
    True
    >>> check_link_format('invalid_link.htm')
    False
    """
    return bool(r_pattern.search(link))


def parse_html_content(html_content: str) -> BeautifulSoup:
    """Parse the HTML content into a BeautifulSoup object."""
    return BeautifulSoup(html_content, "html.parser")


def generate_unique_id(raw_text: str, accession: str) -> str:
    # Generate a unique ID based on the raw text and accession number
    date_pattern = re.search(r"FILED\s*AS\s*OF\s*DATE:(.*?)\n", raw_text)

    if date_pattern:
        filed_date = re.sub(r"\s*", "", date_pattern.group(1))
        return f"{accession[:10]}-{filed_date}-{accession[14:]}"
    else:
        raise DataDockError(message=f"Unable to retrieve the `filed date` for : {accession}", status_code=401)


def clean_text(text: str) -> str:
    # Remove excessive newlines, tabs, and extra spaces
    text = re.sub(r"\n+", "\n", text)  # Replace multiple newlines with a single newline
    text = re.sub(r"\xa0|\n\s*\n", "", text)  # remove non-breaking spaces and consecutive newline characters
    text = re.sub(r"\s{2,}", " ", text)  # Replace multiple spaces with a single space
    text = text.strip()  # Remove leading/trailing whitespace
    return text


def restore_windows_1252_characters(restore_string):
    """
        Replace C1 control characters in the Unicode string s by the
        characters at the corresponding code points in Windows-1252,
        where possible. This should handle some characters, but not all. Hence text should be cleaned more.
    """

    def to_windows_1252(match):
        try:
            return bytes([ord(match.group(0))]).decode('windows-1252')
        except UnicodeDecodeError:
            # No character at the corresponding code point: remove it.
            return ''

    return re.sub(r'[\u0080-\u0099]', to_windows_1252, restore_string)


def child_text(parent: Tag,
               child: str) -> Optional[str]:
    """
    Get the text of the child element if it exists or None
    :param parent: The parent tag
    :param child: The name of the child element
    :return: the text of the child element if it exists or None
    """
    el = parent.find(child)

    if el:
        return el.text.strip()


def child_value(parent: Tag,
                child: str,
                default_value: str = None) -> str:
    """
    Get the text of the value tag within the child tag if it exists or None

    :param parent: The parent tag
    :param child: The name of the child element
    :param default_value: The default value to return if the value is None
    :return: the text of the child element if it exists or None
    """
    el = parent.find(child)
    if el:
        return value_with_footnotes(el)
    return default_value


def value_with_footnotes(tag: Tag,
                         footnote_sep: str = ",") -> str:
    """Get the value from the tag, including footnotes if there are any
    Example: Given this xml
        <underlyingSecurityTitle>
            <value>Class B Common Stock</value>
            <footnoteId id="F2"/>
            <footnoteId id="F3"/>
        </underlyingSecurityTitle>

        return "Class B Common Stock [F2,F3]"
    """
    value_tag = tag.find('value')
    value = value_tag.text if value_tag else ""

    footnote_ids = get_footnote_ids(tag, footnote_sep)
    footnote_str = f"[{footnote_ids}]" if footnote_ids else ""
    if value:
        return f"{value} {footnote_str}" if footnote_str else value
    return footnote_str


def get_footnote_ids(tag: Tag,
                     sep: str = ',') -> str:
    """Get the footnotes from the tag as a string"""
    return sep.join([
        el.attrs.get('id') for el in tag.find_all("footnoteId")
    ])
