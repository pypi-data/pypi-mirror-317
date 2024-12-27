"""
Module: generators.py
========================
Generators for SEC Filing Data Extraction

This module contains functions for scraping relevant links and generating company ticker symbols
based on specific input data, such as HTML content and Central Index Key (CIK). These generators
help automate the process of extracting URLs and corresponding company data from filings and
web-based sources.

Functions:
----------
1. **scrape_r_links**: Scrapes relative links (R-links) from an HTML document and generates
   the full URL for each valid link.

   - **Parameters**:
     - `html_content` (str): The HTML content of the webpage or document to extract links from.
   - **Returns**:
     - `Iterable[str]`: An iterable collection of full URLs corresponding to valid relative
       links found in the HTML content.

2. **ticker_generator**: Generates the company ticker symbol based on the provided CIK and
   returns it in a formatted string.

   - **Parameters**:
     - `cik` (str): The Central Index Key (CIK) representing the company, used for identifying
       the company in SEC filings.
     - `accession_number` (str): The accession number associated with the SEC filing.
   - **Returns**:
     - `str` or `None`: The stock ticker symbol for the company identified by the CIK. If the
       CIK is not found, returns `None`. The result is a string combining the ticker symbol
       and accession number.

Usage:
------
This module is designed for use in web scraping and SEC filing data extraction processes. It includes
utility functions for converting HTML content into usable links and generating ticker symbols for
specific companies based on their CIK. These functions are typically used in processes where
filing data and company-specific information need to be automatically extracted and formatted.

Example Usage:
--------------
# Example 1: Scraping R-links from HTML content
from generators import scrape_r_links

html_content = "<html><a href='/path/to/resource'>Link</a></html>"
for link in scrape_r_links(html_content):
    print(link)

# Example 2: Generating a ticker symbol based on a CIK
from generators import ticker_generator

cik = "320193"
accession_number = "00003456-23-345678"
ticker = ticker_generator(cik, accession_number)
print(ticker)  # Output: 'AAPL-345678'
"""

from typing import Optional, Iterable

from datadock.src.utils import parse_html_content, check_link_format
from datadock.src._constants import SEC_BASE_URL


def scrape_r_links(html_content: str) -> Iterable[str]:
    """
    Scrape and generate a list of relative links (R-links) from the given HTML content.

    Parameters:
    - html_content (str): The HTML content from which to extract the R-links.

    Returns:
    - Iterable[str]: An iterable containing the R-links found in the HTML content.

    This function uses BeautifulSoup to parse the HTML content and extract all anchor tags with 'href' attributes.
    It then checks each link's format using the 'check_link_format' function. If a link is in the correct format,
    it is appended to the resulting list. The function returns the list of R-links.
    """
    if not html_content:
        return []

    # Parse the HTML content using BeautifulSoup
    soup = parse_html_content(html_content)

    # Use a generator expression for efficiency and scalability
    return (
        f"{SEC_BASE_URL}{a_tag['href']}"
        for a_tag in soup.find_all("a", href=True)
        if check_link_format(a_tag["href"])
    )


def ticker_generator(cik: str, accession_number: str) -> Optional[str]:
    """
    Generates and returns the company ticker symbol for a company based on its CIK (Central Index Key).

    Parameters:
    - cik (str): The CIK (Central Index Key) of the company, typically obtained from financial databases.

    Returns:
    - str or None: The stock ticker symbol associated with the given CIK. Returns None if the CIK is not found.

    Company Information:
    - The function has a predefined dictionary of companies with their CIK and ticker symbol.
    - The CIK provided should be in the format 'xxxxxxxxxx-xx-xxxxxx', and leading zeros before the first non-zero
    digit are ignored.

    Example:
    >>> ticker_generator("320193", "00003456-23-345678")
    'META'

    Note:
    - This function uses the CIK to look up the corresponding ticker symbol in the predefined company dictionary.
    - If the CIK is not found or if the provided CIK is not in the expected format, the function returns None.
    """
    companies = {
        "Microsoft": {"cik": "789019", "ticker": "MSFT"},
        "Apple": {"cik": "320193", "ticker": "AAPL"},
        "CVS": {"cik": "64803", "ticker": "CVS"},
        "DELTA": {"cik": "27904", "ticker": "DAL"},
        "EXXON": {"cik": "34088", "ticker": "XOM"},
        "ALPHABET": {"cik": "1652044", "ticker": "GOOGL"},
        "The Goldman Sachs": {"cik": "886982", "ticker": "GS"},
        "Facebook": {"cik": "1326801", "ticker": "META"},
        "Meta": {"cik": "1326801", "ticker": "META"},
        "THE HOME DEPOT": {"cik": "354950", "ticker": "HD"},
        "RITE AID": {"cik": "84129", "ticker": "RAD"},
        "United Parcel Service": {"cik": "1090727", "ticker": "UPS"},
        "3M": {"cik": "66740", "ticker": "MMM"},
    }

    ticker = next(
        (company["ticker"] for company in companies.values() if company["cik"] == cik),
        "DD",
    )
    return f"{ticker}-{accession_number.lstrip('0')}" if ticker else None
