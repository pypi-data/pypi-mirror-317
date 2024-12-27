"""
Module: scrape_financial.py
========================
This module provides a class for managing and filtering scraped SEC financial
results, particularly focusing on `R.htm` documents. It encapsulates the results
from a scraping operation and provides methods to filter, access, and display the
data in a structured way.

Classes:
--------
1. ScrapeFinancialResult:
   - Encapsulates scraping results for SEC filings and provides filtering,
     access, and visualization functionalities.

Methods:
--------
1. __getitem__(self, index: int) -> Optional[str]:
   - Retrieve a filtered `R.htm` link by index.

2. __iter__(self) -> Iterator[str]:
   - Enable iteration over the filtered `R.htm` links.

3. __len__(self) -> int:
   - Return the number of filtered `R.htm` links.

4. get_all_r_links(self) -> List[str]:
   - Retrieve all `R.htm` links from the scraping result.

5. get_filing_id(self) -> str:
   - Retrieve the filing ID from the scraping result.

6. __filtered_links(self) -> List[str]:
   - Filter `R.htm` links to include only R1 to R6.

7. get_financial(self) -> FinancialRequestHandler:
   - Property method to return a `FinancialRequestHandler` object initialized
     with filtered links and filing information.

8. __call__(self) -> Tuple[List[str], str]:
   - Return the filtered links and filing ID when the object is called.

9. __rich__(self) -> Panel:
   - Render the filtered links and filing ID in a rich panel format for visualization.

10. __repr__(self):
   - Provide a string representation of the object using rich formatting.

Usage:
------
Initialize the `ScrapeFinancialResult` class with a tuple of scraped results
and optional filing information. Use methods to access or filter the links.

Example:
--------
    # Example scraped result
    scrape_result = (["R1.htm", "R2.htm", "R7.htm"], "filing123")
    result = ScrapeFinancialResult(scrape_result)

    # Access filtered links
    print(result[0])  # Output: "R1.htm"
    print(len(result))  # Output: 2 (only R1.htm and R2.htm included)

    # Access all raw R.htm links
    all_links = result.get_all_r_links()

    # Display in rich format
    print(result.__rich__())

"""

from typing import Optional, Tuple, List, Iterator

from rich.console import Group
from rich.panel import Panel
from rich.text import Text

from datadock.src.data_class import FilingInfo
from datadock.core._rich_ import repr_rich, display_r_files

from datadock.factory.requestfactory import FinancialRequestHandler, RequestHandlerFactory


class ScrapeFinancialResult:
    """
    A class to manage and filter scraped SEC financial results.

    This class encapsulates scraping results for SEC filings, with a focus
    on `R.htm` links. It provides methods to filter links, retrieve filing
    IDs, and display results in a structured and user-friendly format.

    Attributes:
    -----------
    __scrape_result : Tuple[List[str], str]
        The scraped result containing a list of links and a filing ID.
    __filing_info : FilingInfo, optional
        Additional filing information used for initializing request handlers.

    Methods:
    --------
    - __getitem__(index: int) -> Optional[str]:
        Retrieve a filtered `R.htm` link by index.

    - __iter__() -> Iterator[str]:
        Enable iteration over the filtered `R.htm` links.

    - __len__() -> int:
        Return the number of filtered `R.htm` links.

    - get_all_r_links() -> List[str]:
        Retrieve all `R.htm` links from the scraping result.

    - get_filing_id() -> str:
        Retrieve the filing ID from the scraping result.

    - __filtered_links() -> List[str]:
        Filter `R.htm` links to include only R1 to R6.

    - get_financial -> FinancialRequestHandler:
        Property to return a `FinancialRequestHandler` object.

    - __call__() -> Tuple[List[str], str]:
        Return the filtered links and filing ID.

    - __rich__() -> Panel:
        Render the filtered links and filing ID in a rich panel format.

    - __repr__():
        Provide a string representation of the object using rich formatting.
    """
    def __init__(self, scrape_result: Tuple[List[str],str], filing_info: FilingInfo = None) -> None:
        """
        Initialize the ScrapeFinancialResult object.

        Parameters:
        -----------
        scrape_result : Tuple[List[str], str]
            A tuple containing a list of scraped `R.htm` links and a filing ID.
        filing_info : FilingInfo, optional
            Additional filing information used for initializing request handlers.
        """
        self.__scrape_result = scrape_result
        self.__filing_info = filing_info

    @property
    def get_financial(self) -> FinancialRequestHandler:
        """
        Return a FinancialRequestHandler initialized with filtered links and filing info.

        Returns:
        --------
        FinancialRequestHandler:
            A handler object for managing financial requests based on the filtered links.
        """
        financial_req = RequestHandlerFactory(filing_info=self.__filing_info, url=self.__filtered_links())
        return financial_req()

    def get_all_r_links(self) -> List[str]:
        """Retrieve all `R.htm` links from the scraping result."""
        return self.__scrape_result[0]

    def get_filing_id(self) -> str:
        """Retrieve the filing ID from the scraping result."""
        return self.__scrape_result[1]

    def __getitem__(self, index: int) -> Optional[str]:
        """Retrieve a filtered `R.htm` link by its index."""
        return self.__filtered_links()[index]

    def __iter__(self) -> Iterator[str]:
        """Enable iteration over the filtered `R.htm` links."""
        return iter(self.__filtered_links())

    def __len__(self) -> int:
        """Return the number of filtered `R.htm` links."""
        return len(self.__filtered_links())

    def __filtered_links(self) -> List[str]:
        """Filter `R.htm` links to include only R1 to R6."""
        return [
            link
            for link in self.__scrape_result[0]
            if any(f"R{i}.htm" in link for i in range(1, 7))
        ]

    def __call__(self):
        """Return the filtered links and filing ID as a tuple."""
        return self.__filtered_links(), self.__scrape_result[1]

    def __rich__(self) -> Panel:
        """Render the filtered links and filing ID in a rich panel format."""
        html_links, filing_id = self()

        # Show paging information
        page_info = f"Showing Total of {len(html_links)} scraped R.htm filings"

        return Panel(
            Group(
                display_r_files(
                    html_links,
                    filing_id,
                    index_name="R.htm URLs",
                    title="DataDock Scraped R.htm URLs",
                ),
                Text(page_info),
            ),
        )

    def __repr__(self):
        """Provide a string representation of the object using rich formatting."""
        return repr_rich(self.__rich__())
