"""
Module: _constants.py
=========================
Constants for SEC Filing Processing

This module defines various constants used throughout the SEC filing processing system. These constants represent keys, patterns, or configuration values that are commonly referenced by other modules to maintain consistency and ease of maintenance.

Usage:
------
This module is intended to store constants that are referenced throughout the SEC filing processing system. Instead of hardcoding values directly in multiple places, they are defined here to promote consistency, maintainability, and easier updates.

"""
import re
from typing import Union


SEC_BASE_URL: str = "https://www.sec.gov/"
SEC_DATA_URL: str = "https://www.sec.gov/Archives/edgar/data"


IntString = Union[str, int]
YYYY_MM_DD = "\\d{4}-\\d{2}-\\d{2}"
DATE_PATTERN = re.compile(YYYY_MM_DD)
DATE_RANGE_PATTERN = re.compile(f"({YYYY_MM_DD})?:?(({YYYY_MM_DD})?)?")

text_extensions = (
    ".txt",
    ".htm",
    ".html",
    ".xsd",
    ".xml",
    "XML",
    ".json",
    ".idx",
    ".paper",
)
binary_extensions = (
    ".pdf",
    ".jpg",
    ".jpeg",
    "png",
    ".gif",
    ".tif",
    ".tiff",
    ".bmp",
    ".ico",
    ".svg",
    ".webp",
    ".avif",
    ".apng",
)


barchart = "\U0001F4CA"
ticket = "\U0001F3AB"
page_facing_up = "\U0001F4C4"
classical_building = "\U0001F3DB"


def unicode_for_form(form: str) -> str:
    """
    Returns a unicode character based on the given form type.

    Parameters:
    form (str): The form type to match. It can be one of the following:
        - "10-K", "10-Q", "10-K/A", "10-Q/A", "6-K", "6-K/A"
        - "3", "4", "5", "3/A", "4/A", "5/A"
        - "MA-I", "MA-I/A", "MA", "MA/A"

    Returns:
    str: A unicode character representing the form type. The possible return values are:
        - barchart (U+1F4CA) for "10-K", "10-Q", "10-K/A", "10-Q/A", "6-K", "6-K/A"
        - ticket (U+1F3AB) for "3", "4", "5", "3/A", "4/A", "5/A"
        - classical_building (U+1F3DB) for "MA-I", "MA-I/A", "MA", "MA/A"
        - page_facing_up (U+1F4C4) for any other form type
    """
    if form in ["10-K", "10-Q", "10-K/A", "10-Q/A", "6-K", "6-K/A"]:
        return barchart
    elif form in ["3", "4", "5", "3/A", "4/A", "5/A"]:
        return ticket
    elif form in ["MA-I", "MA-I/A", "MA", "MA/A"]:
        return classical_building
    return page_facing_up
