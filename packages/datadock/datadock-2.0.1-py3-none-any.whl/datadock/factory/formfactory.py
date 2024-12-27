"""
Module: formfactory.py
=====================
This module provides functionality to parse, filter, and save form data extracted from text documents.
It leverages `pyarrow` tables for structured data representation and provides features like Pandas conversion,
data filtering, and rich visualization for terminal display.

Functions:
----------
1. to_table(doc_arrays: List[Tuple[str, str]]) -> pa.Table:
    Converts a list of document title-content pairs into a PyArrow table.

Classes:
--------
1. FormStrategy(ABC):
    An abstract base class to define a strategy for parsing and managing form data.

    Key Features:
    - Abstract parsing method to be implemented by subclasses.
    - Conversion to Pandas DataFrame for analysis or export.
    - Filtering by section titles.
    - Saving data to various file formats.
    - Rich visualization of data for terminal display.

Example Usage:
--------------
    # Create a PyArrow table from document title-content pairs
    doc_arrays = [("Title1", "Content1"), ("Title2", "Content2")]
    table = to_table(doc_arrays)

    # Subclass FormStrategy to implement custom parsing logic
    class MyFormStrategy(FormStrategy):
        def _parse_txt_(self) -> pa.Table:
            # Custom parsing logic
            return to_table(doc_arrays)

    # Use the strategy to manage data
    form_strategy = MyFormStrategy("Sample Document Text")
    print(form_strategy.get_titles())
    form_strategy.save("output_directory", save_formats=[".json", ".csv"])
"""

from os import PathLike
from pathlib import Path
from typing import Optional, List, Union, Tuple
from abc import ABC, abstractmethod

import pandas as pd
import pyarrow as pa

from datadock.src._errors import DataDockError
from datadock.src._constants import IntString

from datadock.core._rich_ import repr_rich
from datadock.core._table_ import SectionsTableDisplay
from datadock.core.filters import filter_by_section_titles


def to_table(doc_arrays: List[Tuple[str, str]]) -> pa.Table:
    """
    Convert a list of document title-content pairs into a PyArrow table.

    Parameters:
    -----------
    doc_arrays : List[Tuple[str, str]]
        A list of tuples where each tuple contains a title and its corresponding content.

    Returns:
    --------
    pa.Table:
        A PyArrow table with two columns: "Title" and "Content".
    """
    keys = [item[0] for item in doc_arrays]
    values = [item[1] for item in doc_arrays]

    key_array = pa.array(keys)
    value_array = pa.array(values)

    table = pa.table({"Title": key_array, "Content": value_array})
    return table


class FormStrategy(ABC):
    """
    An abstract base class to define a strategy for parsing and managing form data.

    This class provides a framework for handling text documents containing form data,
    with methods to parse, filter, and save data in multiple formats. Subclasses should
    implement the `_parse_txt_` method to provide custom parsing logic.

    Attributes:
    -----------
    _txt_document : str, optional
        The raw text of the document being processed.
    _data : pa.Table
        A PyArrow table containing parsed form data with "Title" and "Content" columns.

    Methods:
    --------
    _parse_txt_() -> pa.Table:
        Abstract method to parse the raw text document into a PyArrow table.

    to_pandas(*columns) -> Optional[pd.DataFrame]:
        Convert the parsed data to a Pandas DataFrame.

    filter(titles: Optional[Union[str, List[str]]]) -> FormStrategy:
        Filter the form data by section titles.

    get_titles() -> List[str]:
        Retrieve a list of all section titles from the data.

    save(directory_or_file: PathLike, save_formats: List[str] = [".json"]):
        Save the parsed data to specified file formats in a directory.

    __rich__() -> Panel:
        Render the parsed data as a rich panel for terminal display.

    __repr__() -> str:
        Provide a string representation of the object using rich formatting.
    """
    def __init__(self, txt_document: str = None, section_index: pa.Table = None) -> None:
        """
        Initialize the FormStrategy object.

        Parameters:
        -----------
        txt_document : str, optional
            The raw text of the document being processed.
        section_index : pa.Table, optional
            A pre-parsed PyArrow table with "Title" and "Content" columns.
        """
        self._txt_document = txt_document
        self._data = section_index or self._parse_txt_()

    @abstractmethod
    def _parse_txt_(self) -> pa.Table:
        """
        Abstract method to parse the raw text document into a PyArrow table.

        Subclasses must implement this method to define the parsing logic.

        Returns:
        --------
        pa.Table:
            A PyArrow table with "Title" and "Content" columns.
        """
        pass

    def to_pandas(self, *columns) -> Optional[pd.DataFrame]:
        """
        Convert the parsed data to a Pandas DataFrame.

        Parameters:
        -----------
        *columns : str
            Optional column names to filter the DataFrame.

        Returns:
        --------
        Optional[pd.DataFrame]:
            A Pandas DataFrame containing the parsed data, or None if no data exists.
        """
        if not self._data:
            return None
        data_frame = self._data.to_pandas()
        return data_frame.filter(columns) if len(columns) > 0 else data_frame

    def filter(
        self,
        titles: Optional[Union[str, List[IntString]]] = None,
    ) -> "FormStrategy":
        """
        Filter the form data by section titles.

        Parameters:
        -----------
        titles : Optional[Union[str, List[str]]]
            A single title or a list of titles to filter the data.

        Returns:
        --------
        FormStrategy:
            The current instance with filtered data.
        """
        filing_index = self._data
        section_titles = titles

        if isinstance(section_titles, list):
            section_titles = [str(title) for title in section_titles]

        # Filter by form
        if section_titles:
            filing_index = filter_by_section_titles(filing_index, titles=section_titles)

        self._data = filing_index
        return self

    def get_titles(self) -> List[str]:
        """
        Retrieve a list of all section titles from the data.

        Returns:
        --------
        List[str]:
            A list of section titles.
        """
        return self._data["Title"].to_pylist()

    def save(self, directory_or_file: PathLike, save_formats: List[str] = ".json"):
        """
        Save the parsed data to specified file formats in a directory.

        Parameters:
        -----------
        directory_or_file : PathLike
            Path to the directory or file where the data will be saved.
        save_formats : List[str]
            List of formats to save the data, e.g., [".json", ".csv", ".xlsx"].

        Raises:
        -------
        ValueError:
            If no data exists or unsupported formats are provided.
        IOError:
            If saving the file fails.
        """
        if not self._data:
            raise ValueError("No data to save.")

        try:
            filing_path = Path(directory_or_file)
            filing_path.mkdir(parents=True, exist_ok=True)
        except Exception as error:
            raise DataDockError(f"Unable to access or create the directory: {directory_or_file}. Error: {error}")

        supported_formats = {".json", ".parquet", ".csv", ".xlsx"}
        invalid_formats = [fmt for fmt in save_formats if fmt not in supported_formats]
        if invalid_formats:
            raise ValueError(f"Unsupported formats: {invalid_formats}. Supported formats are: {supported_formats}")

        df = self.to_pandas()  # Convert to Pandas DataFrame for saving

        for fmt in save_formats:
            file_path = filing_path / f"data{fmt}"
            try:
                if fmt == ".json":
                    df.to_json(file_path, orient="records", indent=4)
                elif fmt == ".parquet":
                    df.to_parquet(file_path)
                elif fmt == ".csv":
                    df.to_csv(file_path, index=False)
                elif fmt == ".xlsx":
                    df.to_excel(file_path, index=False)
            except Exception as error:
                raise IOError(f"Failed to save file {file_path}. Error: {error}")

    def __rich__(self) -> "SectionsTableDisplay":
        """Render the parsed data as a rich panel for terminal display."""
        return SectionsTableDisplay(filing_index=self._data)

    def __repr__(self) -> str:
        """Provide a string representation of the object using rich formatting."""
        return repr_rich(self.__rich__())
