"""
Module: filing.py
========================
This module provides utility functions and classes for handling SEC filing data, specifically for fetching, displaying, and processing documents from the EDGAR database.

Functions:
----------
1. `is_valid_form(form_type: IntString) -> bool`: Checks if the given form type is valid based on predefined form types.
2. `format_rich(doc: Any, cik: str, accession: str, form_type: str, dir_view: bool, index_view: bool, txt_view: bool) -> Union[FilingIndexDisplay, str]`: Formats document data into a rich display string depending on the view options and document type.
3. `format_repr(rich_output: str) -> str`: Formats the rich display string into a string representation.

Classes:
--------
1. `FilingListingIndex`: A class for indexing and retrieving SEC filing documents. It handles different views of the filing, including directory, index, and text views. This class also facilitates document scraping and formatting.

   Methods:
   --------
   - `__init__(filing_info: FilingInfo, dir_view: bool, index_view: bool, txt_view: bool) -> None`: Initializes the FilingListingIndex instance.
   - `cik`: Retrieves the Central Index Key (CIK) for the filing.
   - `accession`: Retrieves the accession number associated with the filing.
   - `form_type`: Retrieves the form type of the filing.
   - `dir_view`, `index_view`, `txt_view`: Flags indicating which view of the filing is selected.
   - `html_url`: Generates the URL for the selected view of the filing.
   - `get_r_doc`: Retrieves the result of the scrape request for the financial document.
   - `get_txt_doc`: Retrieves the text document handler for the filing.
   - `open()`: Opens the document for viewing or processing.
   - `__call__()`: Executes the scraping request if not cached.
   - `__rich__()`: Returns a rich-formatted string representing the filing.
   - `__repr__()`: Returns a string representation of the FilingListingIndex instance.

2. `get_filing(cik: str, accession: str, form: IntString, amendment: bool, fill: bool, txt: bool) -> FilingListingIndex`: Fetches filing information from the SEC EDGAR database and returns an instance of `FilingListingIndex` based on the provided parameters.

Error Handling:
---------------
- `ValueError`: Raised if invalid input is provided, such as missing CIK and accession number, or invalid form type.
- `DataDockError`: Raised for incorrect or malformed form types.

This module provides an interface for retrieving, displaying, and processing SEC filings with various views (directory, index, or text), enabling efficient access to important filing data from the EDGAR database.

"""
from typing import Union, List, Any

from datadock.factory.requestfactory import (
    RequestHandlerFactory, DirectoryListingRequestHandler,
    FilingDetailRequestHandler, TxtRequestHandler
)
from datadock.src.utils import build_url
from datadock.src._errors import DataDockError
from datadock.src._constants import IntString, SEC_DATA_URL
from datadock.src.data_class import FilingInfo, FilingTxtDoc

from datadock.form_controller.handler import FormTxtHandler
from datadock.factory.scrape_financials import ScrapeFinancialResult

from datadock.core._table_ import FilingIndexDisplay
from datadock.core._rich_ import repr_rich


form_types = ["8-K", "10-K", "SC 13D", "SC 13G", "D", "13F-HR", "13F-NT"]


def is_valid_form(form_type: IntString) -> bool:
    """
    Checks if the given form type is valid according to the predefined list of form types.

    Parameters:
    form_type (IntString): The form type to be checked.

    Returns:
    bool: True if the form type is valid, False otherwise.
    """
    if form_type.upper() not in form_types:
        return False
    return True


def format_rich(doc: Any, cik: str, accession: str, form_type: str, dir_view: bool, index_view: bool, txt_view: bool) -> Union[FilingIndexDisplay, str]:
    """
    This function formats the given document data into a rich display format based on the provided parameters.

    Parameters:
    doc (Any): The document data to be formatted. It can be a dictionary or an instance of FilingTxtDoc.
    cik (str): The Central Index Key (CIK) of the company.
    accession (str): The accession number of the filing.
    form_type (str): The form type of the filing.
    dir_view (bool): Indicates if the directory listing view is selected.
    index_view (bool): Indicates if the filing index view is selected.
    txt_view (bool): Indicates if the filing TXT view is selected.

    Returns:
    str: The formatted rich display string.
    """
    if isinstance(doc, dict):
        return FilingIndexDisplay(
            form_data=doc["form_data"],
            tables=doc["tables_data"],
            filer_info=doc["filer_data"]
        )
    elif isinstance(doc, FilingTxtDoc):
        return f"TxtRequestHandler(Form Type: {doc.doc_type})"
    return (f"DirectoryListingIndex(\nCIK={cik},\nAccession={accession},\nForm={form_type}\n"
            f"DirView={dir_view},\nIndexView={index_view},\nTxtView={txt_view},\nDocument={doc})")


def format_repr(rich_output: str) -> str:
    """
    Formats the given rich display string into a string representation.

    Parameters:
    rich_output (str): The rich display string to be formatted.
    """
    return repr_rich(rich_output)


class FilingListingIndex:
    """
    A class that handles the indexing and retrieval of SEC filing documents.

    The `FilingListingIndex` class provides methods to access different views (directory, index, or text) of SEC filing data,
    retrieve related documents via URL, and manage document scraping. This class encapsulates information about a specific filing
    and provides ways to access or format data related to that filing.

    Attributes:
    ----------
    cik : str
        The Central Index Key (CIK) identifier for the company filing the document.
    accession : str
        The accession number associated with the filing.
    form_type : str
        The form type of the filing (e.g., "10-K", "8-K").
    dir_view : bool
        A flag indicating whether the directory view is selected.
    index_view : bool
        A flag indicating whether the index view is selected.
    txt_view : bool
        A flag indicating whether the text view is selected.
    html_url : List[str]
        A list containing the URL for the relevant filing, based on the selected view type.
    get_r_doc : ScrapeFinancialResult
        The result of the scrape request for the financial document, if available.
    get_txt_doc : FormTxtHandler
        The result of the text document handling, if available.
    """
    def __init__(self, filing_info: FilingInfo, dir_view: bool = True, index_view: bool = False, txt_view: bool = False) -> None:
        """
        Initializes the FilingListingIndex instance with filing information and view options.

        Parameters:
        ----------
        filing_info : FilingInfo
            The filing information associated with the SEC filing (e.g., CIK, accession number, form type).
        dir_view : bool, optional
            A flag indicating whether to select the directory view (default is True).
        index_view : bool, optional
            A flag indicating whether to select the index view (default is False).
        txt_view : bool, optional
            A flag indicating whether to select the text view (default is False).

        Raises:
        ------
        ValueError
            If more than one of dir_view, index_view, or txt_view is set to True.
        """
        self._filing_info = filing_info

        if sum([dir_view, index_view, txt_view]) != 1:
            raise ValueError("Only one of dir_view or index_view or txt_view can be True.")

        self.__dir_view = dir_view
        self.__index_view = index_view
        self.__txt_view = txt_view
        self.__cached_scrape = None

    @property
    def cik(self) -> str:
        """
        Retrieves the Central Index Key (CIK) for the filing.

        Returns:
        -------
        str
            The CIK of the filing.
        """
        return self._filing_info.cik

    @property
    def accession(self) -> str:
        """
        Retrieves the accession number associated with the filing.

        Returns:
        -------
        str
            The accession number of the filing.
        """
        return self._filing_info.accession_number

    @property
    def form_type(self) -> str:
        """
        Retrieves the form type of the filing (e.g., "10-K", "8-K").

        Returns:
        -------
        str
            The form type of the filing.
        """
        return self._filing_info.form_type

    @property
    def dir_view(self) -> bool:
        """
        Checks if the directory view is selected.

        Returns:
        -------
        bool
            True if the directory view is selected, otherwise False.
        """
        return self.__dir_view

    @property
    def index_view(self) -> bool:
        """
        Checks if the index view is selected.

        Returns:
        -------
        bool
            True if the index view is selected, otherwise False.
        """
        return self.__index_view

    @property
    def txt_view(self)-> bool:
        """
        Checks if the text view is selected.

        Returns:
        -------
        bool
            True if the text view is selected, otherwise False.
        """
        return self.__txt_view

    @property
    def html_url(self) -> List[str]:
        """
        Generates the URL for the selected view of the filing.

        Returns:
        -------
        List[str]
            A list containing the URL for the relevant filing, based on the selected view.
        """
        extra_path = ""
        path_ext = ""

        if self.__index_view:
            extra_path = self.accession
            path_ext = "-index.html"
        elif self.__txt_view:
            extra_path = self.accession
            path_ext = ".txt"

        return [build_url(SEC_DATA_URL, self.cik, self.accession, extra_path=extra_path, path_ext=path_ext)]

    @property
    def get_r_doc(self) -> ScrapeFinancialResult:
        """
        Retrieves the result of the financial document scrape request.

        Returns:
        -------
        ScrapeFinancialResult
            The result of the scrape request, if available.
        """
        if isinstance(self(), tuple):
            return ScrapeFinancialResult(scrape_result=self(), filing_info=self._filing_info)

    @property
    def get_txt_doc(self) -> FormTxtHandler:
        """
        Retrieves the text document handler for the filing.

        Returns:
        -------
        FormTxtHandler
            The handler for the text document, if available.
        """
        if isinstance(self(), FilingTxtDoc):
            return FormTxtHandler(filing_info=self._filing_info, text_doc=self().raw_txt)

    def open(self) -> None:
        """
        Opens the document for viewing or further processing.
        """
        return self.__docdata_().open()

    def __docdata_(self) -> Union[DirectoryListingRequestHandler, FilingDetailRequestHandler, TxtRequestHandler]:
        """
        Retrieves the document handler based on the selected view.

        Returns:
        -------
        Union[DirectoryListingRequestHandler, FilingDetailRequestHandler, TxtRequestHandler]
            The appropriate request handler for the document.
        """
        handler = RequestHandlerFactory(filing_info=self._filing_info, url=self.html_url)
        return handler()

    def __call__(self, *args, **kwargs):
        """
        Executes the scraping request for the document if not already cached.

        Returns:
        -------
        The result of the scraping request.
        """
        if self.__cached_scrape is None:
            self.__cached_scrape = self.__docdata_().scrape()
        return self.__cached_scrape

    def __rich__(self) -> str:
        """Returns a rich-formatted string representing the filing."""
        doc = self()
        return format_rich(doc, self.cik, self.accession, self.form_type, self.dir_view, self.index_view, self.txt_view)

    def __repr__(self) -> str:
        """Returns a string representation of the FilingListingIndex instance."""
        return format_repr(self.__rich__())


def get_filing(
        cik: str = None, accession: str = None,
        form: IntString = None, amendment: bool = False,
        fill: bool = False, txt: bool = False
) -> FilingListingIndex:
    """
    Fetches filing information from the SEC's EDGAR database.

    Args:
        cik (str, optional): Central Index Key (CIK) of the company. Defaults to None.
        accession (str, optional): Accession number of the filing. Defaults to None.
        form (str, optional): Form type of the filing. Defaults to None.
        amendment (bool, optional): Indicates if the filing is an amendment. Defaults to False.
        fill (bool, False, optional): Indicates if the filing detail web page should be viewed
        txt (bool, False, optional): Indicates if the filing detail TXT file should be viewed

    Returns:
        FilingInfo: Filing information object containing CIK, accession number, and form type.
    """
    if not cik or not accession:
        raise ValueError("CIK and accession number are required")

    if form:
        form_type = is_valid_form(form)
        if not form_type:
            error_message = """
            Check correctly the form type. Form types are as follows:
            8-K, 10-K, SC 13D, SC 13G, D.
            Or it could be the case of a missing "-", multiple whitespaces, or lowercases.
            """
            raise DataDockError(message=error_message)

        form = form.upper()

    if amendment:
        form = f"{form}/A"

    filing_info = FilingInfo(cik, accession, form)

    dir_view = not (fill or txt)

    filing_listing = FilingListingIndex(filing_info=filing_info, dir_view=dir_view, index_view=fill, txt_view=txt)

    return filing_listing
