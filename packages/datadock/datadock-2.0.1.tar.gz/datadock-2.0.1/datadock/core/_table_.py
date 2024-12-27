"""
Module: _table_.py
=========================
This module provides functionality for formatting and displaying various components of financial filings.
It includes functions and classes for formatting and displaying form data, tables, and filer information in a rich format.

### Functions:
- format_form_info(form_dict: Dict[str, str]) -> Table:
    Formats the given form dictionary into a rich Table object for display.

- format_table_info(table_data: Dict[str, Any], index: int) -> Table:
    Formats the given table data into a rich Table object for display.

- format_filer_info(filing_data: Dict[str, Any], index: int) -> Table:
    Formats the given filer information into a rich Table object for display.

### Classes:
- FinancialTableDisplay:
    A class for displaying financial table data in a formatted manner. It includes methods to convert the data to a pandas DataFrame, open the table in a browser, and display it in a rich format.

- SectionsTableDisplay:
    A class for displaying the contents of form sections in a formatted manner. It converts form section data into a rich panel for display.

- FilingIndexDisplay:
    A class for displaying filing index data in a rich format. It creates a formatted display of form data, tables, and filer information.

### Exceptions:
- DataDockError:
    Raised if any of the input data is missing or invalid, such as empty dictionaries or missing required keys.

"""

from typing import Dict, List, Any, Union, Optional

import pandas as pd
import pyarrow as pa
from pydantic import BaseModel
from rich import box
from rich.panel import Panel
from rich.console import Group
from rich.table import Table
from rich.text import Text

from datadock.src._errors import DataDockError

from datadock.core._rich_ import repr_rich, financial_rich_table


def format_form_info(form_dict: Dict[str, str]) -> Table:
    """
    This function formats the given form dictionary into a Table object for display.

    Parameters:
    form_dict (Dict[str, str]): A dictionary containing form information. The keys are the form field names, and the values are the corresponding field values.

    Returns:
    Table: A Table object representing the formatted form information.

    Raises:
    DataDockError: If the form dictionary is empty.
    """

    if not form_dict:
        raise DataDockError("""The form dictionary is empty.""")

    items = list(form_dict.items())

    first_two_items = items[:2]
    remaining_items = items[2:]

    form_info_table = Table(
        title="Filing Information",
        box=box.HORIZONTALS,
        show_header=False,
    )
    # Add the first two items to the first row

    if len(first_two_items) > 0:
        form_info_table.add_row(f"[bold]{first_two_items[0][1]}[/bold]")
    if len(first_two_items) > 1:
        form_info_table.add_row(f"[bold]{first_two_items[1][1]}[/bold]")

    # # Add remaining items in a new row
    if remaining_items:
        remaining_data = [
            f"[bold]{key}[/bold]: {value}" for key, value in remaining_items
        ]
        form_info_table.add_row(*remaining_data)

    return form_info_table


def format_table_info(table_data: Dict[str, Any], index: int) -> Table:
    """
    This function formats the given table data into a Table object for display.

    Parameters:
    table_data (Dict[str, Any]): A dictionary containing table information. It should have "headers" and "rows" keys.
        "headers" (List[str]): A list of column headers for the table.
        "rows" (List[List[Any]]): A list of rows, where each row is a list of cell values.

    index (int): The index of the table in the filing. This is used to generate a title for the table.

    Returns:
    Table: A Table object representing the formatted table information.

    Raises:
    DataDockError: If the table dictionary is empty or does not contain the required keys ("headers" and "rows").
    """

    if not table_data:
        raise DataDockError("""The table dictionary is empty.""")

    headers = table_data.get("headers")
    rows = table_data.get("rows")

    table_info = Table(
        title=f"Table {index + 1}: Filing Documents",
        box=box.DOUBLE_EDGE,
    )

    for header in headers:
        table_info.add_column(header, justify="left")
    for row in rows:
        table_info.add_row(*row)

    return table_info


def format_filer_info(filing_data: Dict[str, Any], index: int) -> Table:
    """
    Creates a formatted table for filer information.

    Parameters:
    filing_data (Dict[str, Any]): A dictionary containing filer information. The keys are the filer field names,
        and the values are the corresponding field values.
    index (int): The index of the filer in the filing. This is used to generate a title for the table.

    Returns:
    Table: A Table object representing the formatted filer information.

    Raises:
    DataDockError: If the filing dictionary is empty.
    """

    if not filing_data:
        raise DataDockError("""The filing dictionary is empty.""")

    box_style = box.SQUARE if index % 2 == 0 else box.ROUNDED

    filer_table = Table(
        title=f"Filer Information {index + 1}",
        title_justify="center",
        box=box_style,
        show_header=False,
    )

    for key, value in filing_data.items():
        filer_table.add_row(f"[bold]{key}[/bold]", str(value))

    return filer_table


class FinancialTableDisplay:
    """
    A class used to display financial table data in a formatted manner.

    Attributes:
    _name (str): The name of the financial table.
    _dict_table (pa.Table): The PyArrow table containing the financial data.
    _url (str): The URL to open when the financial table is displayed.

    Methods:
    to_pandas(): Converts the PyArrow table to a pandas DataFrame.
    open(): Opens the financial table in a web browser using the specified URL.
    __rich__(): Returns a rich representation of the financial table for display.
    __repr__(): Returns a string representation of the financial table.
    """

    def __init__(self, name: str, dict_table: pa.Table, url: str) -> None:
        """
        Initializes a new instance of FinancialTableDisplay.

        Parameters:
        name (str): The name of the financial table.
        dict_table (pa.Table): The PyArrow table containing the financial data.
        url (str): The URL to open when the financial table is displayed.
        """
        self._name = name
        self._dict_table = dict_table
        self._url = url

    def to_pandas(self) -> Optional[pd.DataFrame]:
        """
        Converts the PyArrow table to a pandas DataFrame.

        Returns:
        pandas.DataFrame: The converted pandas DataFrame. If the PyArrow table is empty, returns None.
        """
        if not self._dict_table:
            return None
        dataframe = self._dict_table.to_pandas()
        return dataframe

    def open(self) -> None:
        """
        Opens the financial table in a web browser using the specified URL.
        """
        import webbrowser
        webbrowser.open(self._url)

    def __rich__(self) -> Panel:
        """
        Returns a rich representation of the financial table for display.

        Returns:
        rich.panel.Panel: The rich representation of the financial table.
        """
        return Panel(
            Group(
                financial_rich_table(self._dict_table, title=self._name.upper()),
                Text("Showing Financial Statement"),
            ),
            title="DataDock Filings",
        )

    def __repr__(self):
        """
        Returns a string representation of the financial table.
        """
        return repr_rich(self.__rich__())


# I do not think i am using this class
class SectionsTableDisplay:
    """
    A class used to display the contents of form sections in a formatted manner.

    Attributes:
    data (pa.Table): The PyArrow table containing the form section data.

    Methods:
    __init__(filing_index: pa.Table) -> None:
        Initializes a new instance of FormSectionContentsTableDisplay.

    __rich__(self) -> Panel:
        Returns a rich representation of the form section contents for display.

    __repr__(self):
        Returns a string representation of the form section contents.
    """

    def __init__(self, filing_index: pa.Table) -> None:
        """
        Initializes a new instance of FormSectionContentsTableDisplay.

        Parameters:
        filing_index (pa.Table): The PyArrow table containing the form section data.
        """
        self.data = filing_index

    def __rich__(self) -> Panel:
        """
        Returns a rich representation of the form section contents for display.

        Converts the PyArrow table to a pandas DataFrame for easier processing.
        Creates a list to hold all sections.
        Adds each section ID and its content to the list.
        Creates a sub-panel for each section.
        Creates a main panel that contains all sections.

        Returns:
        rich.panel.Panel: The rich representation of the form section contents.
        """
        # Convert the PyArrow table to a pandas DataFrame for easier processing
        df = self.data.to_pandas()

        # Create a list to hold all sections
        sections_content = []

        # Add each section ID and its content to the list
        for section_id, section_text in zip(df["Title"], df["Content"]):
            section_id_text = Text(section_id, style="bold blue")
            section_content_text = Text(section_text)

            # Create a sub-panel for each section
            section_sub_panel = Panel(section_content_text, title=section_id_text)
            sections_content.append(section_sub_panel)

        # Create a main panel that contains all sections
        sections_panel = Panel(
            Group(*sections_content),
            title="DataDock Filings Sections and Contents",
            border_style="green",
        )

        return sections_panel

    def __repr__(self):
        """
        Returns a string representation of the form section contents.
        """
        return repr_rich(self.__rich__())


class FilingIndexDisplay(BaseModel):
    """
    A class used to display the filing index data in a formatted manner.

    Attributes:
    form_data (Dict[str, str]): A dictionary containing form information.
    filer_info (List[Dict[str, Any]]): A list of dictionaries containing filer information.
    tables (List[Dict[str, Union[List[str], Any]]]): A list of dictionaries containing table information.

    Methods:
    __rich__(self) -> Table:
        Returns a rich representation of the filing index data for display.

    __repr__(self) -> str:
        Returns a string representation of the filing index data.
    """

    form_data: Dict[str, str]
    filer_info: List[Dict[str, Any]]
    tables: List[Dict[str, Union[List[str], Any]]]

    def __rich__(self):
        """
        Returns a rich representation of the filing index data for display.

        Creates a Table object with a title and formatting options.
        Adds the filing information table to the Table object.
        Adds table information for each table in the filing index.
        Adds filer information for each filer in the filing index.

        Returns:
        Table: A Table object representing the rich representation of the filing index data.
        """
        box_table = Table(
            title="SEC DataDock Filing",
            title_justify="center",
            box=box.SQUARE,
            show_header=False,
        )

        # Add the filing information table
        form_info = format_form_info(self.form_data)
        # Add a row for CIK and Accession Number
        box_table.add_row(form_info)

        for index, table_data in enumerate(self.tables):
            table_info = format_table_info(table_data, index)
            box_table.add_row(table_info)

        for index, company_info in enumerate(self.filer_info):
            filer_table = format_filer_info(company_info, index)
            box_table.add_row(filer_table)

        return box_table

    def __repr__(self):
        """
        Returns a string representation of the filing index data.
        Calls the __rich__ method to get the rich representation of the filing index data.
        Converts the rich representation to a string using the repr_rich function.
        """
        return repr_rich(self.__rich__())
