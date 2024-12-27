"""
This module initializes the package and makes it possible to use the package's functionality
by exposing key components, classes, and functions. It ensures that the package is properly set up
when imported.
"""

from datadock.src._constants import (
    SEC_BASE_URL, SEC_DATA_URL, IntString, YYYY_MM_DD, DATE_PATTERN, DATE_RANGE_PATTERN,
    text_extensions, binary_extensions, barchart, ticket, page_facing_up, classical_building, unicode_for_form
)
from datadock.src._errors import (
    DataDockError, APIConnectionError, IdentityError, TypeValueError, InvalidRequestMethodError, DataDockServerError
)
from datadock.src.config import check_sec_identity
from datadock.src.logger import CustomLogger
from datadock.src.utils import parse_html_content

from datadock.core._rich_ import (
    add_columns_and_rows, repr_rich, colorize_words,
    format_value, financial_rich_table, display_r_files, df_to_rich_table
)
from datadock.core._table_ import (
    format_form_info, format_table_info, format_filer_info,
    FinancialTableDisplay, SectionsTableDisplay, FilingIndexDisplay
)
from datadock.core._xml_ import parse_xml, xml_namespaces
from datadock.core.filing import (
    form_types, is_valid_form, format_rich, format_repr,
    FilingListingIndex, get_filing
)

__all__ = [
    'SEC_BASE_URL', 'SEC_DATA_URL', 'IntString', 'YYYY_MM_DD', 'DATE_PATTERN', 'DATE_RANGE_PATTERN',
    'check_sec_identity', 'text_extensions', 'binary_extensions', 'barchart', 'ticket', 'page_facing_up',
    'classical_building', 'unicode_for_form', 'DataDockError', 'APIConnectionError', 'IdentityError',
    'TypeValueError', 'InvalidRequestMethodError', 'DataDockServerError', 'CustomLogger',
    'add_columns_and_rows', 'repr_rich', 'colorize_words', 'format_value', 'financial_rich_table',
    'display_r_files', 'df_to_rich_table', 'format_form_info', 'format_table_info', 'format_filer_info',
    'FinancialTableDisplay', 'SectionsTableDisplay', 'FilingIndexDisplay', 'form_types', 'is_valid_form',
    'format_rich', 'format_repr', 'FilingListingIndex', 'get_filing', "parse_xml",
    "xml_namespaces", "parse_html_content"
]
