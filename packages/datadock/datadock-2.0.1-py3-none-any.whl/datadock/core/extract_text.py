"""
Module: extract_text.py
==========================
This module contains functions to extract various types of information from HTML documents using BeautifulSoup.

### Functions:

1. `extract_child_text(tag, child_tag, child_id=None, child_class=None)`:
    - Extracts the text from a child element within a given parent element (`tag`).
    - Searches for the child element based on its tag, and optionally by its `id` or `class`.

    **Parameters:**
    - `tag`: The parent BeautifulSoup Tag object.
    - `child_tag`: The HTML tag of the child element to search for.
    - `child_id`: The optional ID attribute of the child element.
    - `child_class`: The optional class attribute of the child element.

    **Returns:**
    - The text content of the child element, stripped of leading and trailing whitespace. If the child element is not found, an empty string is returned.

2. `extract_form_info(soup, element="div", attributes=None)`:
    - Extracts form information (like form type, accession number, and other details) from a BeautifulSoup object or HTML string.
    - Searches for the form details within specified HTML elements and attributes.

    **Parameters:**
    - `soup`: The BeautifulSoup object or HTML string to parse.
    - `element`: The HTML element to search for within the soup (default is "div").
    - `attributes`: The optional attributes (such as `id`) to match for the HTML element (default is `{"id": "formDiv"}`).

    **Returns:**
    - A dictionary containing extracted form information.

3. `extract_filer_info(soup, element="div", attributes="companyInfo")`:
    - Extracts filer information (such as company name, CIK, and IRS number) from a BeautifulSoup object or HTML string.
    - Searches for div elements matching the provided class (`companyInfo` by default).

    **Parameters:**
    - `soup`: The BeautifulSoup object, HTML string, or Tag to parse.
    - `element`: The HTML element to search for (default is "div").
    - `attributes`: The class attribute to match for the element (default is `"companyInfo"`).

    **Returns:**
    - A list of dictionaries containing extracted filer information.

4. `extract_tables_info(soup, element="table", attributes=None)`:
    - Extracts table information from a BeautifulSoup object or HTML string.
    - Searches for tables based on the provided element type and optional attributes.

    **Parameters:**
    - `soup`: The BeautifulSoup object, HTML string, or Tag to parse.
    - `element`: The HTML element to search for (default is "table").
    - `attributes`: Optional attributes to match for the HTML element.

    **Returns:**
    - A list of dictionaries, where each dictionary represents a table found in the soup. Each dictionary contains the table's headers and rows.

5. `get_filing_data_html(doc_html)`:
    - Extracts form, table, and filer information from a given HTML document.
    - Uses other extraction functions to obtain specific details from the HTML document.

    **Parameters:**
    - `doc_html`: The HTML document from which to extract data.

    **Returns:**
    - A dictionary containing extracted data: "form_data", "tables_data", and "filer_data".

6. `extract_financial_data(document)`:
    - Scrapes the document to extract all data from the first table found in the HTML document.
    - Converts the extracted data into a PyArrow table for further processing.

    **Parameters:**
    - `document`: The HTML document to extract data from.

    **Returns:**
    - A `pyarrow.Table` containing the extracted data from the first valid table found in the document. If no tables are found or valid data cannot be extracted, returns `None`.

7. `extract_header_pattern(raw_text, form_type)`:
    - Extracts a specific form section from raw text by searching for the `<DOCUMENT>` tags and matching the form type.

    **Parameters:**
    - `raw_text`: The raw HTML or text content containing the form data.
    - `form_type`: The form type to search for in the document (e.g., "10-K").

    **Returns:**
    - A `FilingTxtDoc` object containing the extracted section, or raises an error if the specified form type is not found.
"""

import re
from typing import Union, Optional, Dict, List, Any

from bs4 import BeautifulSoup, Tag
import pyarrow as pa
import pandas as pd

from datadock.src.data_class import FilingTxtDoc
from datadock.src._errors import DataDockError
from datadock.src.utils import parse_html_content

from datadock.core.filters import filer_status


def extract_child_text(
    tag: Tag, child_tag: str, child_id: str = None, child_class: str = None
) -> str:
    """
    Extracts the text from a child element within a given parent element.

    Parameters:
    tag (Tag): The parent BeautifulSoup Tag object.
    child_tag (str): The HTML tag of the child element to search for.
    child_id (str, optional): The ID attribute of the child element. If provided, this will be used to find the child element.
    child_class (str, optional): The class attribute of the child element. If provided, this will be used to find the child element.

    Returns:
    str: The text content of the child element, stripped of leading and trailing whitespace. If the child element is not found, an empty string is returned.
    """
    if child_id:
        child = tag.find(child_tag, {"id": child_id})
    elif child_class:
        child = tag.find(child_tag, {"class": child_class})
    else:
        child = tag.find(child_tag)

    return child.text.strip() if child else ""


def extract_form_info(
    soup: Union[Tag, BeautifulSoup],
    element: Union[Tag, str] = "div",
    attributes: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    """
    Extracts form information from a BeautifulSoup object or HTML string.

    Parameters:
    soup (Union[Tag, BeautifulSoup]): The BeautifulSoup object or HTML string to parse.
    element (Union[Tag, str], optional): The HTML element to search for within the soup. Defaults to "div".
    attributes (Optional[Dict[str, str]], optional): The attributes to match for the HTML element. Defaults to {"id": "formDiv"}.

    Returns:
    Dict[str, Any]: A dictionary containing the extracted form information.
    """

    # Parse the soup if a string is provided
    if isinstance(soup, str):
        soup = BeautifulSoup(soup, "html.parser")

    # Set default attributes if none are provided
    if attributes is None:
        attributes = {"id": "formDiv"}

    # Extract Filing Data from First View
    form_data = {}

    # Find the main form div
    form_div = soup.find(element, attributes)
    if form_div:
        # Extract Form Type and Accession Number
        form_data["Form Type"] = extract_child_text(
            form_div, "div", child_id="formName"
        )
        form_data["Accession Number"] = extract_child_text(
            form_div, "div", child_id="secNum"
        )

        # Extract other form details from the formGrouping divs
        info_groups = form_div.find_all("div", class_="formGrouping")
        for group in info_groups:
            info_heads = group.find_all("div", class_="infoHead")
            infos = group.find_all("div", class_="info")

            for head, info in zip(info_heads, infos):
                form_data[head.text.strip()] = info.text.strip()

    return form_data


def extract_filer_info(
    soup: Union[str, BeautifulSoup, Tag],
    element: Union[Tag, str] = "div",
    attributes: Optional[str] = "companyInfo",
) -> List[Dict[str, Any]]:
    """
    Extracts filer information from a BeautifulSoup object or HTML string.

    Parameters:
    soup (Union[str, BeautifulSoup, Tag]): The BeautifulSoup object, HTML string, or Tag to parse.
    element (Union[Tag, str], optional): The HTML element to search for within the soup. Defaults to "div".
    attributes (Optional[str], optional): The class attribute to match for the HTML element. Defaults to "companyInfo".

    Returns:
    List[Dict[str, Any]]: A list of dictionaries, where each dictionary contains the extracted filer information.
    """
    
    company_data_list = []

    # Parse the soup if it's a string
    if isinstance(soup, str):
        soup = BeautifulSoup(soup, "html.parser")

    # Find all divs that match the specified class (e.g., companyInfo)
    company_info_divs = soup.find_all(element, class_=attributes)

    for company in company_info_divs:
        form_data = {}

        # Extract the company name and issuer/filer status
        company_name_elem = company.find("span", class_="companyName")
        if company_name_elem:
            company_name = company_name_elem.text.split(" (")[0].strip()
            status = filer_status(company_name_elem.text)
            form_data["Company Name"] = company_name
            form_data["Status"] = status

        # Extract CIK
        cik_elem = company.find("acronym", {"title": "Central Index Key"})
        if cik_elem:
            form_data["CIK"] = cik_elem.find_next("a").text.split(" (")[0].strip()

        # Extract IRS No., File No., and SIC
        ident_info_p = company.find("p", class_="identInfo")
        if ident_info_p:
            # IRS No.
            irs_no_elem = ident_info_p.find(
                "acronym", {"title": "Internal Revenue Service Number"}
            )
            if irs_no_elem:
                form_data["IRS No."] = irs_no_elem.find_next("strong").text.strip()

            # File No.
            file_no_elem = ident_info_p.find(
                "a", href=lambda href: href and "filenum" in href
            )
            if file_no_elem:
                form_data["File No."] = file_no_elem.find("strong").text.strip()

            # SIC (Standard Industrial Code)
            sic_elem = ident_info_p.find(
                "acronym", {"title": "Standard Industrial Code"}
            )
            if sic_elem:
                form_data["SIC"] = sic_elem.find_next("b").text.strip()

        # Append the company data to the list
        company_data_list.append(form_data)

    return company_data_list


def extract_tables_info(
    soup: Union[str, BeautifulSoup, Tag],
    element: Union[Tag, str] = "table",
    attributes: Optional[Dict[str, str]] = None,
) -> List[Dict[str, Any]]:
    """
    Extracts table information from a BeautifulSoup object or HTML string.

    Parameters:
    soup (Union[str, BeautifulSoup, Tag]): The BeautifulSoup object, HTML string, or Tag to parse.
    element (Union[Tag, str], optional): The HTML element to search for within the soup. Defaults to "table".
    attributes (Optional[Dict[str, str]], optional): The attributes to match for the HTML element. Defaults to None.

    Returns:
    List[Dict[str, Any]]: A list of dictionaries, where each dictionary represents a table found in the soup.
    Each dictionary contains the table headers and rows.
    """
    if isinstance(soup, str):
        soup = BeautifulSoup(soup, "html.parser")

    # Find all elements matching the specified tag and attributes
    tables = (
        soup.find_all(element, attrs=attributes)
        if attributes
        else soup.find_all(element)
    )

    # List to hold table data
    all_table_data = []

    # Loop through each table and extract data
    for table in tables:
        table_data = []
        rows = table.find_all("tr")

        # Extract column headers
        headers = [th.get_text(strip=True) for th in rows[0].find_all("th")]

        # Extract row data
        for row in rows[1:]:
            columns = row.find_all("td")
            row_data = [col.get_text(strip=True) for col in columns]
            table_data.append(row_data)

        # Store table headers and data
        all_table_data.append({"headers": headers, "rows": table_data})

    return all_table_data


def get_filing_data_html(
    doc_html: str,
) -> Dict[str, Union[Dict[str, Any], List[Dict[str, Any]], List[Dict[str, Any]]]]:
    """
    This function extracts form, table, and filer information from a given HTML document.

    Parameters:
    doc_html (str): The HTML document to extract data from.

    Returns:
    Dict[str, Union[Dict[str, Any], List[Dict[str, Any]], List[Dict[str, Any]]]]: A dictionary containing the extracted data.
    The dictionary has three keys: "form_data", "tables_data", and "filer_data".
    - "form_data" contains the extracted form information as a dictionary.
    - "tables_data" contains the extracted table information as a list of dictionaries, where each dictionary represents a table.
    - "filer_data" contains the extracted filer information as a list of dictionaries, where each dictionary represents a filer.
    """
    soup = parse_html_content(doc_html)
    form_data_html = extract_form_info(soup)
    tables_data_html = extract_tables_info(soup)
    filer_data_html = extract_filer_info(soup)
    return {
        "form_data": form_data_html,
        "tables_data": tables_data_html,
        "filer_data": filer_data_html,
    }


def extract_financial_data(document: str) -> Optional[pa.Table]:
    """
    Scrape the document from the URL and extract all data from <table> tags.

    Parameters:
    document (str): The HTML document to extract data from.

    Returns:
    Optional[pa.Table]: A pyarrow Table containing the extracted data from the first valid table found in the document.
                        If no tables are found or valid data cannot be extracted, returns None.
    """
    soup = parse_html_content(document)

    table = soup.find("table")

    if not table:
        raise ValueError("No table found in this HTML content")

    headers = []
    rows = []
    for tr in table.find_all("tr"):
        if tr.find("th"):
            # This is a header row, group its <th> content into a list
            header = [th.get_text(strip=True) for th in tr.find_all("th")]
            headers.append(header)
        else:
            # This is a data row, extract <td> content
            row = [td.get_text(strip=True) for td in tr.find_all("td")]
            rows.append(row)

    headers_length = len(headers)
    if headers_length > 1:
        first_header_length = len(headers[0])
        second_header_length = len(headers[1])
    else:
        first_header_length = len(headers[0]) if headers else 0
        second_header_length = 0  # No second header row

    first_row_length = len(rows[0]) if rows else 0

    if headers and first_row_length > first_header_length:
        # Add an empty string after the first index in the first header list
        headers[0].insert(1, "")

        # If there's a second header, add an empty string at the start
        if headers_length > 1:
            headers[1].insert(0, "")

    # Ensure headers and rows are consistent
    if headers:
        # Flatten headers if multiple header rows exist
        if len(headers) > 1:
            flattened_headers = [
                f"{h1} {h2}".strip() for h1, h2 in zip(headers[0], headers[1])
            ]
        else:
            flattened_headers = headers[0]
    else:
        flattened_headers = []

    # Ensure header length matches row length by padding if necessary
    max_columns = max(len(flattened_headers), max(len(row) for row in rows))
    flattened_headers += [""] * (max_columns - len(flattened_headers))

    # Convert headers and rows to a DataFrame
    data = pd.DataFrame(rows, columns=flattened_headers)

    # Convert the DataFrame to a PyArrow Table
    arrow_table = pa.Table.from_pandas(data)

    # return {"headers": headers, "rows": rows}
    return arrow_table


def extract_header_pattern(raw_text: str, form_type: str) -> Optional[FilingTxtDoc]:

    form_type = form_type.upper()
    raw_form_type = []

    # Regex to find <DOCUMENT> tags
    doc_start_pattern = re.compile(r"<DOCUMENT>")
    doc_end_pattern = re.compile(r"</DOCUMENT>")
    type_pattern = re.compile(r"<TYPE>[^\n]+")

    doc_start_is = [x.end() for x in doc_start_pattern.finditer(raw_text)]
    doc_end_is = [x.start() for x in doc_end_pattern.finditer(raw_text)]
    doc_types = [x[len("<TYPE>") :] for x in type_pattern.findall(raw_text)]

    # Create a loop to go through each section type and save only the 10-K section in the dictionary
    for doc_type, doc_start, doc_end in zip(doc_types, doc_start_is, doc_end_is):
        raw_form_type.append(doc_type)
        if doc_type == form_type:
            return FilingTxtDoc(doc_type=doc_type, raw_txt=raw_text[doc_start:doc_end])

    doc_form_type = raw_form_type[0]
    # if form_type not in filing_txt_doc.doc_type:
    raise DataDockError(message=f"""No {form_type} section not found in the document.
    Please check the form type or the document type you passed.
    Do you mean '{doc_form_type}'??""")
