"""
Module: _control_d_.py
=====================
This module provides functionality to parse Form D text documents.
It extracts detailed information about the issuer, offering data,
sales compensation, and signatures, and organizes it into a structured
pyarrow Table for further processing.

Classes:
--------
1. FormDController:
   - Parses a Form D text document and organizes the extracted information
     into a structured table format.

Methods:
--------
1. FormDController._parse_txt_:
   - Parses the input Form D text document and extracts relevant sections
     into a pyarrow Table.

2. FormDController._collect_d_details:
   - Static helper method that organizes extracted Form D data into
     a list of key-value pairs.

Usage:
------
To use this module, initialize the `FormDController` class with a valid
Form D text document and call the `_parse_txt_` method.

Example:
--------
    controller = FormDController(txt_document)
    result_table = controller._parse_txt_()
    print(result_table)

"""

from typing import List, Tuple
import pyarrow as pa

from datadock.core._xml_ import parse_xml

from datadock.factory.formfactory import FormStrategy, to_table

from datadock.src.models import (
    FilingSchema, Issuer, SignatureIssuer, OfferingData,
    SalesCompensationRecipient, Person
)


class FormDController(FormStrategy):
    """
    A controller class for parsing Form D text documents.

    This class processes a Form D document in text format, extracts details
    like issuer information, offering data, related persons, sales compensation,
    and signature blocks, and organizes the data into a structured pyarrow Table.

    Methods:
    --------
    _parse_txt_() -> pa.Table:
        Parses the input Form D document and converts the extracted data
        into a pyarrow Table.

    _collect_d_details(...) -> List[Tuple[str, str]]:
        A static helper method to organize and format the extracted data
        into a list of (key, value) pairs for tabular representation.
    """
    def _parse_txt_(self) -> pa.Table:
        """
        Parses the Form D text document and returns the extracted data as a pyarrow Table.

        Steps:
        ------
        1. Parses the input text document into an XML structure.
        2. Extracts components such as filing schema, issuer details,
           related person information, offering data, and signature details.
        3. Uses the `_collect_d_details` helper method to format the extracted
           data into key-value pairs.
        4. Converts the key-value pairs into a pyarrow Table for structured storage.

        Returns:
        --------
        pyarrow.Table:
            A table containing the extracted Form D details.
        """

        root_xpath = parse_xml(self._txt_document)

        # Extract components from the XML structure
        form_schema = FilingSchema.from_xml(root_xpath)
        issuer = Issuer.from_xml(root_xpath)
        person = Person.from_xml(root_xpath)
        signature_issuer = SignatureIssuer.from_xml(root_xpath)
        offering_data = OfferingData.from_xml(root_xpath)
        sales_compensation = SalesCompensationRecipient.from_xml(root_xpath)

        # Collect details
        form_d_details = self._collect_d_details(
            form_schema, issuer, person, signature_issuer, offering_data, sales_compensation
        )
        return to_table(form_d_details)

    @staticmethod
    def _collect_d_details(form_schema: FilingSchema, issuer: Issuer, person: Person,
                           signature_issuer: SignatureIssuer, offering_data: OfferingData,
                           sales_compensation: SalesCompensationRecipient) -> List[Tuple[str, str]]:
        """
        Collects and organizes Form D details into a list of (key, value) tuples.

        Parameters:
        -----------
        form_schema : FilingSchema
            Schema information of the filing, including submission type.
        issuer : Issuer
            Details about the issuer, including name, CIK, and address.
        person : Person
            Information about related persons, such as names, addresses,
            and relationships.
        signature_issuer : SignatureIssuer
            Signature block information for the issuer, including authorized
            representatives and dates.
        offering_data : OfferingData
            Offering data details, such as security types, amounts sold,
            use of proceeds, and investor information.
        sales_compensation : SalesCompensationRecipient
            Sales compensation information, including recipient names,
            CRD numbers, and solicitation details.

        Returns:
        --------
        List[Tuple[str, str]]:
            A list of key-value pairs representing the extracted Form D details.

        Example Output:
        ---------------
        [
            ("Schema Version", "1.0"),
            ("Issuer CIK", "123456789"),
            ("Issuer Entity Name", "ABC Corporation"),
            ("Offering Data Total Amount Sold", "$5,000,000"),
            ("Signature Name", "John Doe"),
            ...
        ]
        """

        # Avoid redundant calls
        issuer_address = issuer.primary_address
        year_of_inc = issuer.year_of_incorporation
        security = offering_data.security
        signatures = signature_issuer.signatures
        investors = offering_data.investors
        sales_commission = offering_data.sales_commission_finders_fees
        offering_sales = offering_data.offering_sales_amounts
        business_transaction = offering_data.business_combination_transaction
        use_of_proceeds = offering_data.use_of_proceeds

        return [
            ("Schema Version", form_schema.filing_schema),
            ("Submission Type", form_schema.submission_type),
            ("Test or Live", form_schema.test_or_live),
            ("Issuer CIK", issuer.cik),
            ("Issuer Entity Type", issuer.entity_type),
            ("Issuer Entity Name", issuer.entity_name),
            ("Entity Other Description", issuer.entity_other_types_desc),
            ("Issuer Phone Number", issuer.phone_number),
            ("Issuer Street1 Address", issuer_address.street1),
            ("Issuer Street2 Address", issuer_address.street2),
            ("Issuer City", issuer_address.city),
            ("Issuer State or Country", issuer_address.state_or_country),
            ("Issuer State or Country Description", issuer_address.state_or_country_description),
            ("Issuer Zip Code", issuer_address.zipcode),
            ("Edgar Previous Names", issuer.edgar_previous_names),
            ("Issuer Previous Names", issuer.issuer_previous_names),
            ("Jurisdiction", issuer.jurisdiction),
            ("Year of Incorporation", year_of_inc.year_of_inc),
            ("Year of Incorporation Value", year_of_inc.year_of_inc_value),
            ("Related Person First Names", person.first_name),
            ("Related Person Last Names", person.last_name),
            ("Related Person Street1", person.street1),
            ("Related Person Street2", person.street2),
            ("Related Person City", person.city),
            ("Related Person State or Country", person.state_or_country),
            ("Related Person State or Country Description", person.state_or_country_description),
            ("Related Person Zip Code", person.zip_code),
            ("Related Person Relationship", person.relationships),
            ("Related Person Clarification", person.relationship_clarifications),
            ("Offering Data Industry Group", offering_data.industry_group.industry_group_type),
            ("Offering Data Investment Type", offering_data.investment_fund),
            ("Offering Data Is 40 Act", offering_data.is_40_act),
            ("Offering Data Revenue/Aggregate Range", offering_data.revenue_range),
            ("Offering Data Federal Exemptions/Exclusions", offering_data.federal_exemptions),
            ("Offering Data Amendment", offering_data.is_new),
            ("Offering Data Previous Number", offering_data.previous_accession),
            ("Offering Data Date of First Sale/Yet to Occur", offering_data.date_of_first_sale),
            ("Offering Data Duration Offering", offering_data.more_than_one_year),
            ("Offering Data Security Type [Equity]", security.equity),
            ("Offering Data Security Type [Debt]", security.debt),
            ("Offering Data Security Type [Pooled Investment]", security.pooled_investment),
            ("Offering Data Security Type [Tenant]", security.tenant_security),
            ("Offering Data Security Type [Mineral]", security.mineral_security),
            ("Offering Data Security Type [Options]", security.options),
            ("Offering Data Security Type [Acquire Security]", security.security_acquire),
            ("Offering Data Security Type [Other]", security.other),
            ("Offering Data Security Type [Description]", security.other_description),
            ("Offering Data Business Combination", business_transaction.is_business_combination),
            ("Offering Data Business Clarification", business_transaction.clarification_of_response),
            ("Offering Data Minimum Investment", offering_data.minimum_investment),
            ("Offering Data Total Amount Offering", offering_sales.total_offering_amount),
            ("Offering Data Total Amount Sold", offering_sales.total_amount_sold),
            ("Offering Data Total Amount Remaining", offering_sales.total_remaining),
            ("Offering Data Clarification", offering_sales.clarification_of_response),
            ("Offering Data Investors", investors.has_non_accredited_investors),
            ("Offering Data Total Invested", investors.total_already_invested),
            ("Offering Data Number of Investors", investors.num_non_accredited_investors),
            ("Offering Data Sales Commission", sales_commission.sales_commission),
            ("Offering Data Total Sales Commission", sales_commission.finders_fees),
            ("Offering Data Total Sales Commission Clarification", sales_commission.clarification_of_response),
            ("Offering Data Use of Proceeds Gross", use_of_proceeds.gross_proceeds_used),
            ("Offering Data Use of Proceeds Estimate", use_of_proceeds.is_estimate),
            ("Offering Data Use of Proceeds Clarification", use_of_proceeds.clarification_of_response),
            ("Offering Sales Compensation Names", sales_compensation.name),
            ("Offering Sales Compensation CRD Number", sales_compensation.crd_name),
            ("Offering Sales Compensation BD Name", sales_compensation.associated_bd_name),
            ("Offering Sales Compensation BD CRD Number", sales_compensation.associated_bd_crd),
            ("Offering Sales Compensation Address", sales_compensation.street1),
            ("Offering Sales Compensation Address 2", sales_compensation.street2),
            ("Offering Sales Compensation City", sales_compensation.city),
            ("Offering Sales Compensation State/Country", sales_compensation.state_or_country),
            ("Offering Sales Compensation State/Country Description", sales_compensation.state_or_country_desc),
            ("Offering Sales Compensation Zip Code", sales_compensation.zip_code),
            ("Offering Sales Compensation Solicitation", sales_compensation.solicitation),
            ("Signature Authorization", signature_issuer.authorized_representative),
            ("Signature Name", signatures.signature_name),
            ("Signature Title", signatures.title),
            ("Signature Name of Issuer Name", signature_issuer.issuer_name),
            ("Signature Name of Signer", signatures.name_of_signer),
            ("Signature Date", signatures.date)
        ]
