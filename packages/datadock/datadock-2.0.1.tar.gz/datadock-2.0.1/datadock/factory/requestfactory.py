"""
Module: requestfactory.py
========================
Request Handlers for SEC Filing Data Retrieval and Scraping

This module contains classes designed to handle various types of SEC filings and
associated documents. Each handler is tailored to a specific kind of request or
filing type, providing methods for fetching, scraping, and processing data.

Classes:
--------
1. DirectoryListingRequestHandler:
    Handles directory listing pages from the SEC's website.
    - Fetches and scrapes links from index or directory pages.
    - Provides a method to open the page in a web browser.

    Methods:
    - __init__(filing_info: FilingInfo, url: str = None): Initializes the handler.
    - _fetch_document(): Fetches the directory page document using HTTP GET.
    - open(): Opens the directory page in the default web browser.
    - scrape(): Scrapes R.htm links and generates a unique filing ID.

2. FilingDetailRequestHandler:
    Handles detailed filing pages from the SEC.
    - Scrapes specific filing information from a detailed filing page.

    Methods:
    - __init__(filing_info: FilingInfo, url: str = None): Initializes the handler.
    - _fetch_document(): Fetches the filing detail page using HTTP GET.
    - open(): Opens the filing detail page in the default web browser.
    - scrape(): Extracts filing metadata such as form type, filing date, and registrant details.

3. TxtRequestHandler:
    Handles plain text (.txt) filing documents.
    - Extracts and processes data from plain text versions of SEC filings.

    Methods:
    - __init__(filing_info: FilingInfo, url: str): Initializes the handler.
    - _fetch_document(): Fetches the plain text document using HTTP GET.
    - open(): Opens the plain text document in the default web browser.
    - scrape(): Extracts structured data from the plain text document based on header patterns.

4. FinancialRequestHandler:
    Handles financial data tables from SEC filings.
    - Focuses on scraping financial statements such as balance sheets, income statements, etc.

    Methods:
    - __init__(filing_info: FilingInfo, urls: List[str] = None): Initializes the handler with multiple URLs.
    - _fetch_document(url: str): Fetches a financial data document using HTTP GET.
    - scrape_statement(statement_type: str): Scrapes data for a specific financial statement.
    - cover_page(): Extracts data from the cover page (first URL).
    - balance_sheet(): Extracts data from the balance sheet (second URL).
    - income(): Extracts data from the income statement (third URL).
    - loss(): Extracts data from the loss statement (fourth URL).
    - net_income(): Extracts data from the net income statement (fifth URL).
    - consolidation(): Extracts data from the consolidation statement (sixth URL).

5. RequestHandlerFactory:
    A factory class to dynamically create the appropriate request handler based on the URL.
    - Determines the type of handler to return using the file extension or URL pattern.

    Methods:
    - __init__(url: List[str], filing_info: FilingInfo): Initializes the factory with a list of URLs and filing info.
    - __call__(): Returns an instance of the appropriate request handler.

Usage:
------
These classes are designed to work in conjunction, allowing for modular and
dynamic handling of SEC filings. Use `RequestHandlerFactory` to create handlers
based on the type of URL being processed.

Example:
--------
    # Initialize filing info and URL list
    filing_info = FilingInfo(cik="0000320193", accession_number="0000320193-23-000001")
    urls = ["https://www.sec.gov/Archives/edgar/data/320193/000032019323000001/index.htm"]

    # Create a handler using the factory
    factory = RequestHandlerFactory(url=urls, filing_info=filing_info)
    handler = factory()

    # Fetch and scrape data
    data = handler.scrape()

    # Process data based on the handler type
    if isinstance(handler, FinancialRequestHandler):
        balance_sheet_data = handler.balance_sheet()
"""

import webbrowser
from typing import Union, Optional, List, Tuple, Dict, Any

import pyarrow as pa
from pydantic import BaseModel, field_validator

from datadock.src._errors import DataDockError
from datadock.src._base_request import BaseRequest
from datadock.src.data_class import FilingInfo, FilingTxtDoc
from datadock.src.generators import scrape_r_links, ticker_generator
from datadock.src.utils import check_url_ext

from datadock.core.extract_text import get_filing_data_html, extract_financial_data, extract_header_pattern
from datadock.core._table_ import FinancialTableDisplay


class DirectoryListingRequestHandler(BaseRequest):
    """
    Handles directory listing pages from the SEC website.

    This class is responsible for fetching, scraping, and processing data from
    directory or index pages that contain links to SEC filings. It also provides
    a method to open the page in the default web browser.

    Attributes:
    ----------
    _url : str
        The URL of the directory page.
    _filing_info : FilingInfo
        An object containing metadata about the filing, such as CIK and accession number.
    """
    def __init__(self, filing_info: FilingInfo, url: str = None) -> None:
        """
        Initialize the DirectoryListingRequestHandler.

        Parameters:
        ----------
        filing_info : FilingInfo
            An object containing metadata about the filing, such as CIK and accession number.
        url : str, optional
            The URL of the directory page. If not provided, defaults to None.
        """
        super().__init__()
        self._url = url or None
        self._filing_info = filing_info

    def _fetch_document(self) -> Optional[str]:
        """
        Fetch the SEC document using the HTTP GET method.

        Returns:
        -------
        Optional[str]
            The content of the directory page as a string, or None if the request fails.
        """
        return self._request("GET", self._url)

    def open(self) -> None:
        """
        Open the directory page in the default web browser.

        This method uses the `webbrowser` module to open the URL in the system's
        default browser.
        """
        webbrowser.open(self._url)

    def scrape(self) -> Tuple[List[str], str]:
        """
        Scrape R.htm links and generate a unique filing ID.

        Extracts all R.htm links from the directory page and creates a unique
        filing identifier based on the CIK and accession number.

        Returns:
        -------
        Tuple[List[str], str]
            A tuple containing:
            - A list of R.htm links scraped from the page.
            - A unique filing ID generated from the CIK and accession number.
        """
        response = self._fetch_document()
        scrape_result = list(scrape_r_links(response)), ticker_generator(
            self._filing_info.cik, self._filing_info.accession_number
        )
        return scrape_result


class FilingDetailRequestHandler(BaseRequest):
    """
    Handles detailed filing pages from the SEC website.

    This class is responsible for fetching, scraping, and processing data from
    detailed filing pages. It also provides a method to open the page in the
    default web browser.

    Attributes:
    ----------
    _url : str
        The URL of the filing detail page.
    _filing_info : FilingInfo
        Metadata about the filing, such as CIK and accession number.
    """
    def __init__(self, filing_info: FilingInfo, url: str = None) -> None:
        """
        Initialize the FilingDetailRequestHandler.

        Parameters:
        ----------
        filing_info : FilingInfo
            Metadata about the filing, such as CIK and accession number.
        url : str, optional
            The URL of the filing detail page. If not provided, defaults to None.
        """
        super().__init__()
        self._url = url or None
        self._filing_info = filing_info  # i do not think this is necessary

    def _fetch_document(self) -> Optional[str]:
        """
        Fetch the SEC filing detail page using the HTTP GET method.

        Returns:
        -------
        Optional[str]
            The content of the filing detail page as a string, or None if the
            request fails.
        """
        return self._request("GET", self._url)

    def open(self) -> None:
        """
        Open the filing detail page in the default web browser.

        This method uses the `webbrowser` module to open the URL in the system's
        default browser.
        """
        webbrowser.open(self._url)

    def scrape(self) -> Dict[str, Any]:
        """
        Scrape filing information from the detail page.

        Extracts structured filing information from the HTML content of the
        filing detail page.

        Returns:
        -------
        Dict[str, Any]
            A dictionary containing parsed filing information extracted from
            the HTML content.
        """
        response = self._fetch_document()
        filing_info = get_filing_data_html(response)
        return filing_info


class TxtRequestHandler(BaseRequest):
    """
    Handles requests for SEC TXT filing documents.

    This class is responsible for fetching, opening, and scraping textual
    filings in `.txt` format from the SEC website. It processes the filing to
    extract relevant information.

    Attributes:
    ----------
    _url : str
        The URL of the TXT filing document.
    _filing_info : FilingInfo
        Metadata about the filing, such as the form type.
    """
    def __init__(self, filing_info: FilingInfo, url: str) -> None:
        """
        Initialize the TxtRequestHandler.

        Parameters:
        ----------
        filing_info : FilingInfo
            Metadata about the filing, such as form type.
        url : str
            The URL of the TXT filing document.
        """
        super().__init__()
        self._url = url or None
        self._filing_info = filing_info  # i do not think this is necessary

    def _fetch_document(self) -> Optional[str]:
        """
        Fetch the SEC TXT filing document using the HTTP GET method.

        Returns:
        -------
        Optional[str]
            The content of the TXT filing document as a string, or None if the
            request fails.
        """
        return self._request("GET", self._url)

    def open(self) -> None:
        """
        Open the TXT Filing document (.txt) page in the default web browser.

        This method uses the `webbrowser` module to open the URL in the system's
        default browser.
        """
        webbrowser.open(self._url)

    def scrape(self) -> FilingTxtDoc:
        """
        Scrape the content of the TXT filing document.

        Extracts and parses filing information from the TXT document's raw text
        content.

        Returns:
        -------
        FilingTxtDoc
            A structured representation of the extracted filing information.
        """
        response = self._fetch_document()
        filing_info = extract_header_pattern(raw_text=response, form_type=self._filing_info.form_type)
        return filing_info


class FinancialRequestHandler(BaseRequest):
    """
    Handles requests and parsing of SEC financial filing documents.

    This class is responsible for fetching and scraping financial statements
    from a list of URLs corresponding to different sections of SEC financial
    filings. It supports various types of financial statements such as balance
    sheets, income statements, and more.

    Attributes:
    ----------
    __urls : List[str]
        A list of URLs for different sections of the financial filing.
    __filing_info : FilingInfo
        Metadata about the filing, such as the form type.
    """
    def __init__(self, filing_info: FilingInfo, urls: Union[List[str]] = None) -> None:
        """
        Initialize the FinancialRequestHandler.

        Parameters:
        ----------
        filing_info : FilingInfo
            Metadata about the filing, such as form type.
        urls : Union[List[str]]
            A list of URLs corresponding to different sections of the financial
            filing.
        """
        super().__init__()
        self.__urls = urls
        self.__filing_info = filing_info

    def _fetch_document(self, url: str = None) -> Optional[str]:
        """
        Fetch a financial statement document using the HTTP GET method.

        Parameters:
        ----------
        url : str, optional
            The URL of the financial statement document to fetch.

        Returns:
        -------
        Optional[str]
            The content of the financial statement document as a string, or None
            if the request fails.
        """
        return self._request("GET", url)

    def __scrape(self, url: str) -> Optional[Tuple[pa.Table, str]]:
        """
        Scrape and extract financial data from a document.

        Parameters:
        ----------
        url : str
            The URL of the financial statement document to scrape.

        Returns:
        -------
        Optional[Tuple[pa.Table, str]]
            A tuple containing the financial data as an Arrow table and the URL
            of the scraped document.
        """
        response = self._fetch_document(url)
        filing_info = extract_financial_data(response)
        return filing_info, url

    def scrape_statement(self, statement_type: str) -> "FinancialTableDisplay":
        """
        Scrape a specific type of financial statement.

        This method identifies the URL corresponding to the requested statement
        type and scrapes the data.

        Parameters:
        ----------
        statement_type : str
            The type of financial statement to scrape. Supported values:
            - "cover_page"
            - "balance_sheet"
            - "income"
            - "loss"
            - "net_income"
            - "consolidation"

        Returns:
        -------
        FinancialTableDisplay
            A structured display object containing the scraped data for the
            specified statement type.

        Raises:
        ------
        DataDockError
            If the specified statement type is invalid or its index exceeds the
            number of available URLs.
        """
        statement_mapping = {
            "cover_page": 0,
            "balance_sheet": 1,
            "income": 2,
            "loss": 3,
            "net_income": 4,
            "consolidation": 5,
        }
        index = statement_mapping.get(statement_type)
        if index is None or index >= len(self.__urls):
            raise DataDockError(f"Invalid statement type: {statement_type}")

        data_tables = self.__scrape(self.__urls[index])
        return FinancialTableDisplay(statement_type, data_tables[0], data_tables[1])


class RequestHandlerFactory(BaseModel):
    """
    A factory class for creating appropriate request handlers for SEC filings.

    This class dynamically determines the type of handler needed based on the
    URL's characteristics and returns an instance of the corresponding handler
    class. It supports the following handler types:
    - `DirectoryListingRequestHandler`
    - `TxtRequestHandler`
    - `FilingDetailRequestHandler`
    - `FinancialRequestHandler`

    Attributes:
    ----------
    url : List[str]
        A list of URLs representing the filing documents to process.
    filing_info : FilingInfo
        Metadata about the filing, such as the CIK and form type.
    """
    url: List[str]
    filing_info: FilingInfo

    @field_validator('url')
    def url_list(cls, value) -> List[str]:
        """
        Ensure the URL attribute is always a list.

        Converts a single URL string into a list if necessary.

        Parameters:
        ----------
        value : str or List[str]
            The URL or list of URLs provided.

        Returns:
        -------
        List[str]
            A list of URLs.

        Example:
        -------
        >>> RequestHandlerFactory.url_list("http://example.com")
        ["http://example.com"]
        """
        if isinstance(value, str):
            return [value]
        return value

    def __call__(self, *args, **kwargs) -> Union[
        DirectoryListingRequestHandler,
        TxtRequestHandler,
        FilingDetailRequestHandler,
        FinancialRequestHandler
    ]:
        """
        Create and return the appropriate request handler instance based on the URL.

        This method examines the first URL in the list and determines its type
        using the `check_url_ext` function. It then returns the corresponding
        request handler instance.

        Returns:
        -------
        Union[DirectoryListingRequestHandler, TxtRequestHandler, FilingDetailRequestHandler, FinancialRequestHandler]
            An instance of the appropriate request handler class.

        Raises:
        ------
        DataDockError
            If the URL list is empty or the type of handler cannot be determined.

        Example:
        -------
        >>> filing_info = FilingInfo(cik="1234", accession_number="1234", form_type="9-K")
        >>> factory = RequestHandlerFactory(url=["http://example.com"], filing_info=filing_info)
        >>> handler = factory()
        """
        if not self.url:
            raise DataDockError("URL list cannot be empty.")

        url_check = check_url_ext(self.url[0])

        if url_check == "index":
            return FilingDetailRequestHandler(self.filing_info, self.url[0])
        elif url_check == "txt":
            return TxtRequestHandler(self.filing_info, self.url[0])
        elif url_check == "Rfile":
            return FinancialRequestHandler(self.filing_info, self.url)
        return DirectoryListingRequestHandler(self.filing_info, self.url[0])
