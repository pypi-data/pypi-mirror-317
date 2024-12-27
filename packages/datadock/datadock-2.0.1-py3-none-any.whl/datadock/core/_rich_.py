"""
Module: __rich__.py
=====================
This module is for generating and displaying rich tables using the `rich` library.

This module contains various functions to generate rich tables for displaying different types of data, including financial tables and other structured information. The functions also provide functionality to format data, colorize words, and convert data structures like Pandas DataFrames or PyArrow tables into rich table representations.

Functions:

- add_columns_and_rows(rich_table: Table, df: pd.DataFrame, index_name: Optional[str] = None):
    Adds columns and rows to a given `rich` table from a Pandas DataFrame.

- repr_rich(renderable) -> str:
    Renders a `rich` object (e.g., Table, Text) to a string for capturing console output.

- colorize_words(words, colors=None) -> Text:
    Colorizes a list of words with a list of colors.

- format_value(value: Any) -> str:
    Formats a value for display in the rich table, ensuring compatibility for various types of data.

- financial_rich_table(df: Union[pa.Table, List[Any]], index_name: Optional[str] = None, title: str = "", title_style: str = "", table_box: box.Box = box.SQUARE) -> Table:
    Creates a rich table to display financial data. Converts PyArrow Table to Pandas DataFrame if needed and then populates a `rich` table.

- display_r_files(arrow_table: Union[pa.Table, List[Any]], filing_id: str = None, index_name: Optional[str] = None, title: str = "", title_style: str = "", table_box: box.Box = box.SQUARE) -> Table:
    Creates a rich table to display R file information. Accepts either a PyArrow Table or a list of items and adds them to the table.

- df_to_rich_table(df: Union[pd.DataFrame, pa.Table], index_name: Optional[str] = None, title: str = "", title_style: str = "", max_rows: int = 20, table_box: box.Box = box.SIMPLE_HEAVY) -> Table:
    Converts a DataFrame or PyArrow Table into a rich table, with options for limiting the number of rows and styling.
"""
from typing import Union, Optional, List, Any
import itertools

import pandas as pd
import pyarrow as pa
from rich import box
from rich.table import Table
from rich.text import Text


table_styles = {
    "Form": "yellow2",
    "FilingDate": "deep_sky_blue1",
    "Filing Date": "deep_sky_blue1",
    "File Number": "sandy_brown",
    "CIK": "dark_sea_green4",
    "Accepted Date": "dark_slate_gray1",
    "Accession Number": "light_coral",
    "HTML URLs": "yellow2",
    "Document File No": "yellow2",
    "R.htm URLs": "yellow2",
}


def add_columns_and_rows(rich_table: Table, df: pd.DataFrame, index_name: Optional[str] = None):
    """Add columns and rows to the rich table from a DataFrame."""
    # Add columns
    for column in df.columns:
        column_type = str(df[column].dtype)
        column_style = table_styles.get(column_type, "white")  # Default style
        rich_table.add_column(column, style=column_style, justify="left")

    # Add rows
    for index in range(len(df)):
        row_data = [format_value(df[col].iloc[index]) for col in df.columns]
        rich_table.add_row(*row_data)

    # Add index column if specified
    if index_name:
        rich_table.add_column(index_name, style="white", justify="right")
        for index in range(len(df)):
            rich_table.add_row(*[""] + [format_value(df[col].iloc[index]) for col in df.columns])


def repr_rich(renderable) -> str:
    """
    This renders a rich object to a string

    It implements one of the methods of capturing output listed here

    https://rich.readthedocs.io/en/stable/console.html#capturing-output

     This is the recommended method if you are testing console output in unit tests

        from io import StringIO
        from rich.console import Console
        console = Console(file=StringIO())
        console.print("[bold red]Hello[/] World")
        str_output = console.file.getvalue()

    :param renderable:
    :return:
    """
    from rich.console import Console

    console = Console()
    with console.capture() as capture:
        console.print(renderable)
    str_output = capture.get()
    return str_output


def colorize_words(words, colors=None) -> Text:
    """Colorize a list of words with a list of colors" """
    colors = colors or ["deep_sky_blue3", "red3", "dark_sea_green4"]
    colored_words = []
    color_cycle = itertools.cycle(colors)

    for word in words:
        color = next(color_cycle)
        colored_words.append((word, color))

    return Text.assemble(*colored_words)


def format_value(value: Any) -> str:
    """Format the value for display in the rich table."""
    if isinstance(value, list):
        return ", ".join(map(str, value))  # Join list items with a comma
    return str(value)


def financial_rich_table(
        df: Union[pa.Table, List[Any]],
        index_name: Optional[str] = None,
        title: str = "",
        title_style: str = "",
        table_box: box.Box = box.SQUARE,
) -> Table:
    """
    Create a rich table for financial data display.

    This function takes a DataFrame or a PyArrow Table, along with optional parameters for table styling and formatting.
    It converts the input data to a pandas DataFrame if it's a PyArrow Table, and then creates a rich table using the
    provided parameters.

    Parameters:
    - df (Union[pa.Table, List[Any]]): The input data to be displayed in the table. It can be a PyArrow Table or a list of items.
    - index_name (Optional[str]): The name of the index column. Default is None.
    - title (str): The title of the table. Default is an empty string.
    - title_style (str): The style of the table title. Default is an empty string.
    - table_box (box.Box): The box style of the table. Default is box.SQUARE.

    Returns:
    - Table: A rich table object containing the financial data.
    """
    rich_table = Table(
        box=table_box,
        row_styles=["bold", ""],
        title=title,
        title_style=title_style or "bold",
        title_justify="center",
    )

    if isinstance(df, pa.Table):
        # Convert pyarrow table to pandas DataFrame for easier manipulation
        df = df.to_pandas()

    add_columns_and_rows(rich_table=rich_table, df=df, index_name=index_name)

    return rich_table


def display_r_files(
    arrow_table: Union[pa.Table, List[Any]],
    filing_id: str = None,
    index_name: Optional[str] = None,
    title: str = "",
    title_style: str = "",
    table_box: box.Box = box.SQUARE,
) -> Table:
    """
    Create a rich table to display R files information.

    Parameters:
    - arrow_table (Union[pa.Table, List[Any]]): The input data to be displayed in the table. It can be a pyarrow Table or a list of items.
    - filing_id (str, optional): The ID of the filing. Default is None.
    - index_name (Optional[str], optional): The name of the index column. Default is None.
    - title (str, optional): The title of the table. Default is an empty string.
    - title_style (str, optional): The style of the table title. Default is an empty string.
    - table_box (box.Box, optional): The box style of the table. Default is box.SQUARE.

    Returns:
    - Table: A rich table object containing the R files information.
    """
    rich_table = Table(
        box=table_box,
        row_styles=["bold", ""],
        title=title,
        title_style=title_style or "bold",
        title_justify="center",
        caption=filing_id,
    )
    index_name = str(index_name) if index_name else ""
    index_style = table_styles.get(index_name)
    rich_table.add_column(
        index_name, style=index_style, header_style=index_style, justify="right"
    )

    if isinstance(arrow_table, pa.Table):
        df = arrow_table.to_pandas()
        add_columns_and_rows(rich_table=rich_table, df=df, index_name=index_name)
    elif isinstance(arrow_table, list):
        # If it's a list, we can display it directly
        for link in arrow_table:
            rich_table.add_row(link)

    return rich_table


def df_to_rich_table(
    df: Union[pd.DataFrame, pa.Table],
    index_name: Optional[str] = None,
    title: str = "",
    title_style: str = "",
    max_rows: int = 20,
    table_box: box.Box = box.SIMPLE_HEAVY,
) -> Table:
    """
    Convert a dataframe to a rich table

    :param index_name: The name of the index
    :param df: The dataframe to convert to a rich Table
    :param max_rows: The maximum number of rows in the rich Table
    :param title: The title of the Table
    :param title_style: The title of the Table
    :param table_box: The rich box style e.g. box.SIMPLE
    :return: a rich Table
    """
    if isinstance(df, pa.Table):
        # For speed, learn to sample the head and tail of the pyarrow table
        df = df.to_pandas()

    rich_table = Table(
        box=table_box,
        row_styles=["bold", ""],
        title=title,
        title_style=title_style or "bold",
        title_justify="center",
    )
    index_name = str(index_name) if index_name else ""
    index_style = table_styles.get(index_name)
    rich_table.add_column(
        index_name, style=index_style, header_style=index_style, justify="right"
    )

    add_columns_and_rows(rich_table=rich_table, df=df, index_name=index_name)

    if len(df) > max_rows:
        head = df.head(max_rows // 2)
        tail = df.tail(max_rows // 2)
        data_for_display = pd.concat(
            [
                head,
                pd.DataFrame([{col: "..." for col in df.columns}], index=["..."]),
                tail,
            ]
        )
    else:
        data_for_display = df

    data_for_display = data_for_display.reset_index()

    for value_list in data_for_display.values.tolist():
        row = [str(x) for x in value_list]
        rich_table.add_row(*row)

    return rich_table
