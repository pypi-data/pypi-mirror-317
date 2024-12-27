"""
Module: _control_13fnt_.py
=========================
This module provides functionality to parse Form 13F-NT text documents.
It extracts various fields from the document, including submission details,
manager information, signature block data, and summary page details,
and converts them into a structured pyarrow Table.

Classes:
--------
1. Form13FNTController:
   - Parses the input Form 13F-NT document and collects relevant information
     into a structured table format.

Methods:
--------
1. Form13FNTController._parse_txt_:
   - Entry point for parsing a Form 13F-NT document.
   - Extracts relevant XML components and uses a helper method to collect
     details into key-value pairs.

2. Form13FNTController._collect_13nt_details:
   - Static method that organizes and formats extracted fields into a list
     of (key, value) tuples.

Usage:
------
To use this module, initialize the `Form13FNTController` class with a valid
Form 13F-NT document and call its `_parse_txt_` method.

Example:
--------
    controller = Form13FNTController(txt_document)
    result_table = controller._parse_txt_()
    print(result_table)

"""

from typing import List, Tuple

import pyarrow as pa

from datadock.core._xml_ import parse_xml

from datadock.factory.formfactory import FormStrategy, to_table

from datadock.src.models import (
    FilingSchema, Flags, FileIdentity,
    CalendarReport, FileManager, FileReport, SignatureBlock,
    SummaryPage, Form13NTOtherManagersInfo
)


class Form13FNTController(FormStrategy):
    """
    Controller class for parsing Form 13F-NT text documents.

    Methods:
    --------
    _parse_txt_ :
        Parses the input Form 13F-NT document and collects relevant information
        into a structured table format.

    _collect_13nt_details_ :
        Static method that organizes and formats extracted fields into a list
        of (key, value) tuples.

    """

    def _parse_txt_(self) -> pa.Table:
        """
        Parses the input Form 13F-NT document and collects relevant information
        into a structured table format.

        Parameters:
        -----------
        self : Form13FNTController
            The instance of the Form13FNTController class.

        Returns:
        --------
        pa.Table
            A structured table containing the parsed information.

        """

        root_xpath = parse_xml(self._txt_document)
        
        # Extract components from the XML structure
        form_schema = FilingSchema.from_xml(root_xpath)
        flags = Flags.from_xml(root_xpath)
        file_identity = FileIdentity.from_xml(root_xpath)
        report_calendar = CalendarReport.from_xml(root_xpath)
        file_manager = FileManager.from_xml(root_xpath)
        file_report = FileReport.from_xml(root_xpath)
        signature_block = SignatureBlock.from_xml(root_xpath)
        summary = SummaryPage.from_xml(root_xpath)
        other_managers = Form13NTOtherManagersInfo.from_xml(root_xpath)
        
        # Collect details
        form_13fnt_details = self._collect_13nt_details_(
            form_schema, flags, file_identity, report_calendar, file_manager,
            file_report, signature_block, summary, other_managers
        )
        return to_table(form_13fnt_details)

    @staticmethod
    def _collect_13nt_details_(
            form_schema: FilingSchema,
            flags: Flags, file_identity: FileIdentity, report_calendar: CalendarReport, file_manager: FileManager,
            file_report: FileReport, signature_block: SignatureBlock,
            summary: SummaryPage, other_managers: Form13NTOtherManagersInfo) -> List[Tuple[str, str]]:
        """
        Organizes and formats extracted fields into a list of (key, value) tuples.

        Parameters:
        -----------
        form_schema : FilingSchema
            The parsed schema information from the Form 13F-NT document.
        flags : Flags
            The parsed flags information from the Form 13F-NT document.
        file_identity : FileIdentity
            The parsed file identity information from the Form 13F-NT document.
        report_calendar : CalendarReport
            The parsed report calendar information from the Form 13F-NT document.
        file_manager : FileManager
            The parsed file manager information from the Form 13F-NT document.
        file_report : FileReport
            The parsed file report information from the Form 13F-NT document.
        signature_block : SignatureBlock
            The parsed signature block information from the Form 13F-NT document.
        summary : SummaryPage
            The parsed summary page information from the Form 13F-NT document.
        other_managers : Form13NTOtherManagersInfo
            The parsed other managers information from the Form 13F-NT document.

        Returns:
        --------
        List[Tuple[str, str]]
            A list of tuples containing the extracted field names and their corresponding values.

        """

        # This is to reduce repeated calls
        address = file_manager.address
        signatures = signature_block.signatures

        return [
            ("Schema Version", form_schema.filing_schema),
            ("Submission Type", form_schema.submission_type),
            ("Test or Live", form_schema.test_or_live),
            ("Confirmation Flag", str(flags.confirm_copy_flag)),
            ("Return Flag", str(flags.return_copy_flag)),
            ("Override Internet Flag", str(flags.override_internet_flag)),
            ("CIK", file_identity.cik),
            ("CCC", file_identity.ccc),
            ("Period of Report", report_calendar.period_of_report),
            ("Report Calendar Quarter", report_calendar.report_calendar_quarter),
            ("Filing Manager Name", file_manager.name),
            ("Street 1 Address", address.street1),
            ("Street 2 Address", address.street2),
            ("City", address.city),
            ("State or Country", address.state_or_country),
            ("Zip Code", address.zipcode),
            ("File Report Type", file_report.report_type),
            ("Form 13F Number", file_report.form_13),
            ("CRD Number", file_report.crd),
            ("SEC File Number", file_report.sec_file_num),
            ("Provide Information", file_report.provide_info),
            ("Signature Block Name", signatures.signature_name),
            ("Signature Block Title", signatures.title),
            ("Signature Block Phone", signature_block.phone),
            ("Signature Block Name of Signer", signatures.name_of_signer),
            ("Signature Block City", signature_block.city),
            ("Signature Block State", signature_block.state),
            ("Signature Block Date", signatures.date),
            ("Summary Page Other Managers Count", summary.other_managers),
            ("Summary Page Table Entry Total", summary.table_entry),
            ("Summary Page Table Value Total", summary.table_value),
            ("Summary Page Confidential", summary.confidential),
            ("Other Managers Info CIK", other_managers.cik),
            ("Other Managers Info Form 13 Num", other_managers.form13_number),
            ("Other Managers Info Name", other_managers.name)
        ]
