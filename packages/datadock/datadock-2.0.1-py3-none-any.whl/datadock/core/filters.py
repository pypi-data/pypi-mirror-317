"""
Module: filters.py
=========================
This module provides various utility functions to filter and process financial data using PyArrow tables.
The functions allow filtering by specific attributes such as form type, CIK, accession number, file number,
date ranges, and section titles. Additionally, the module includes helper functions for determining filer types
and parsing date strings into start and end dates.

Functions:
- filer_status: Determines the type of filer based on the provided text.
- filter_by_form: Filters a PyArrow Table by form types, with an option to include amendments.
- filter_by_cik: Filters a PyArrow Table by CIK numbers.
- filter_by_accession: Filters a PyArrow Table by accession numbers.
- filter_by_file_no: Filters a PyArrow Table by file numbers.
- extract_dates: Splits a date or date range into a start date and an end date.
- filter_by_date: Filters a PyArrow Table based on a specific date or date range.
- filter_by_section_titles: Filters a PyArrow Table based on section titles.

The functions in this module are designed to facilitate data extraction and analysis from SEC filing documents,
where filtering by various criteria like form type, CIK, and date is commonly required. Each function is modular
and accepts parameters specific to the filtering criteria, returning a filtered PyArrow Table.
"""
import re
from typing import Union, List, Optional, Tuple
from datetime import datetime, date

import pyarrow as pa
import pyarrow.compute as pc
from fastcore.basics import listify

from datadock.src._constants import IntString, DATE_RANGE_PATTERN
from datadock.src.logger import CustomLogger


logging = CustomLogger().logger


def filer_status(text: str) -> str:
    """
    Determine the type of filer based on the provided text.

    Parameters:
    text (str): The input text to analyze.

    Returns:
    str: The type of filer. One of "Issuer", "Filer", or "Reporting".
    """
    if "Issuer" in text:
        return "Issuer"
    elif "Filer" in text:
        return "Filer"
    elif "Reporting" in text:
        return "Reporting"


def filter_by_form(
    data: pa.Table, form_type: Union[str, List[str]], amendments: bool = False
) -> pa.Table:
    """
    Filter a PyArrow Table based on form types and, optionally, include amendments.

    Parameters:
    data (pa.Table): The input PyArrow Table containing form data.
    form_type (Union[str, List[str]]): The form type(s) to filter for. Can be a single form type or a list of form types.
    amendments (bool, optional): If True, include amendments for the specified form types. Defaults to False.

    Returns:
    pa.Table: A new PyArrow Table containing only the filtered form data.
    """
    forms = [str(item) for item in listify(form_type)]
    if amendments:
        forms = list(
            set(forms + [f"{val}/A" for val in forms])
        )  # Add amendment indicator to forms
    data = data.filter(pc.is_in(data["Form"], pa.array(forms)))
    return data


def filter_by_cik(data: pa.Table, cik: Union[IntString, List[IntString]]) -> pa.Table:
    """
    Filter a PyArrow Table based on CIK numbers.

    This function accepts a PyArrow Table and a list of CIK numbers (either as integers or strings).
    It returns a new PyArrow Table containing only the rows that match the specified CIK numbers.

    Parameters:
    data (pa.Table): The input PyArrow Table containing financial data.
    cik (Union[IntString, List[IntString]]): The CIK number(s) to filter for. Can be a single CIK number or a list of CIK numbers.

    Returns:
    pa.Table: A new PyArrow Table containing only the rows that match the specified CIK numbers.
    """
    # Ensure that cik is a list of strings ... it can accept int like form 3, 4, 5
    ciks = [str(el) for el in listify(cik)]
    data = data.filter(pc.is_in(data["CIK"], pa.array(ciks)))
    return data


def filter_by_accession(
    data: pa.Table, accession_number: Union[IntString, List[IntString]]
) -> pa.Table:
    """
    Filter a PyArrow Table based on accession numbers.

    This function accepts a PyArrow Table and a list of accession numbers (either as integers or strings).
    It returns a new PyArrow Table containing only the rows that match the specified accession numbers.

    Parameters:
    data (pa.Table): The input PyArrow Table containing financial data.
    accession_number (Union[IntString, List[IntString]]): The accession number(s) to filter for.
        Can be a single accession number or a list of accession numbers.

    Returns:
    pa.Table: A new PyArrow Table containing only the rows that match the specified accession numbers.
    """
    # Ensure that accession is a list of strings ... it can accept int like form 3, 4, 5
    accession = [str(el) for el in listify(accession_number)]
    data = data.filter(pc.is_in(data["Accession Number"], pa.array(accession)))
    return data


def filter_by_file_no(
    data: pa.Table, file_no: Union[IntString, List[IntString]]
) -> pa.Table:
    """
    Filter a PyArrow Table based on file numbers.

    This function accepts a PyArrow Table and a list of file numbers (either as integers or strings).
    It returns a new PyArrow Table containing only the rows that match the specified file numbers.

    Parameters:
    data (pa.Table): The input PyArrow Table containing financial data.
    file_no (Union[IntString, List[IntString]]): The file number(s) to filter for.
        Can be a single file number or a list of file numbers.

    Returns:
    pa.Table: A new PyArrow Table containing only the rows that match the specified file numbers.
    """
    # Ensure that file_no is a list of strings ... it can accept int like form 3, 4, 5
    file_number = [str(el) for el in listify(file_no)]
    data = data.filter(pc.is_in(data["File Number"], pa.array(file_number)))
    return data


def extract_dates(input_date: str) -> Tuple[Optional[str], Optional[str], bool]:
    """
    Split a date or a date range into start_date and end_date
        split_date("2022-03-04")
          2022-03-04, None, False
       split_date("2022-03-04:2022-04-05")
        2022-03-04, 2022-04-05, True
       split_date("2022-03-04:")
        2022-03-04, None, True
       split_date(":2022-03-04")
        None, 2022-03-04, True
    :param input_date: The date to split
    :return:
    """
    log = logging
    match = re.match(DATE_RANGE_PATTERN, input_date)
    if match:
        start_date, _, end_date = match.groups()
        try:
            start_date_tm = (
                datetime.strptime(start_date, "%Y-%m-%d") if start_date else None
            )
            end_date_tm = datetime.strptime(end_date, "%Y-%m-%d") if end_date else None
            if start_date_tm or end_date_tm:
                return start_date_tm, end_date_tm, ":" in input_date
        except ValueError:
            log.error(
                f"The date {input_date} cannot be extracted using date pattern YYYY-MM-DD"
            )
    raise Exception(
        f"""
    Cannot extract a date or date range from string {input_date}
    Provide either 
        1. A date in the format "YYYY-MM-DD" e.g. "2022-10-27"
        2. A date range in the format "YYYY-MM-DD:YYYY-MM-DD" e.g. "2022-10-01:2022-10-27"
        3. A partial date range "YYYY-MM-DD:" to specify dates after the value e.g.  "2022-10-01:"
        4. A partial date range ":YYYY-MM-DD" to specify dates before the value  e.g. ":2022-10-27"
    """
    )


def filter_by_date(
    data: pa.Table, date_input: Union[str, datetime], date_col: str
) -> pa.Table:
    """
    Filter a PyArrow Table based on a specific date or date range.

    This function accepts a PyArrow Table, a date or date range (as a string or datetime object),
    and a column name representing the date field. It converts the date or date range to a
    timestamp format and filters the table based on the specified date or date range.

    Parameters:
    data (pa.Table): The input PyArrow Table containing financial data.
    date_input (Union[str, datetime]): The date or date range to filter for.
        This can be a string in the format "YYYY-MM-DD" or "YYYY-MM-DD:YYYY-MM-DD",
        or a datetime object.
    date_col (str): The name of the column in the table that contains the date field.

    Returns:
    pa.Table: A new PyArrow Table containing only the rows that match the specified date or date range.
    """
    # If datetime convert to string
    if isinstance(date_input, date) or isinstance(date_input, datetime):
        date_input = date_input.strftime("%Y-%m-%d")

    # Extract the date parts ... this should raise an exception if we cannot
    date_parts = extract_dates(date_input)
    start_date, end_date, is_range = date_parts

    # Convert Date column to timestamp[s]
    data = data.set_column(
        data.schema.get_field_index(date_col),
        date_col,
        pc.cast(data[date_col], pa.timestamp("s")),
    )

    if is_range:
        filtered_data = data
        if start_date:
            filtered_data = filtered_data.filter(
                pc.field(date_col) >= pc.scalar(start_date)
            )
        if end_date:
            filtered_data = filtered_data.filter(
                pc.field(date_col) <= pc.scalar(end_date)
            )
    else:
        # filter by filings on date
        filtered_data = data.filter(pc.field(date_col) == pc.scalar(start_date))
    return filtered_data


def filter_by_section_titles(
    data: pa.Table, titles: Union[IntString, List[IntString]]
) -> pa.Table:
    """
    Filter a PyArrow Table based on section titles.

    This function accepts a PyArrow Table and a list of section titles (either as integers or strings).
    It returns a new PyArrow Table containing only the rows that match the specified section titles.

    Parameters:
    data (pa.Table): The input PyArrow Table containing financial data. This table should have a column named "Title"
        containing the section titles.
    titles (Union[IntString, List[IntString]]): The section title(s) to filter for.
        Can be a single section title or a list of section titles. This function will accept integers or strings.

    Returns:
    pa.Table: A new PyArrow Table containing only the rows that match the specified section titles.
    """
    # Ensure that titles is a list of strings ... it can accept int like form 3, 4, 5
    title = [str(el) for el in listify(titles)]
    data = data.filter(pc.is_in(data["Title"], pa.array(title)))
    return data
