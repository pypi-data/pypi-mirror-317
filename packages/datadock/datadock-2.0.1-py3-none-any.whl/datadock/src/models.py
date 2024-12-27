"""
Module: models.py
===================
This module contains Pydantic models for various tasks related to the application.
Each model is designed to validate and serialize data associated with different aspects of the system,
such as user information, configuration settings, data inputs, and responses.

Models in this file use Pydantic's data validation capabilities to ensure proper format, types, and required fields
are maintained for different use cases.
"""
from typing import Optional

from lxml import etree
from bs4 import Tag
from rich import box
from rich.console import Group
from rich.table import Table
from rich.panel import Panel
from pydantic import BaseModel

from datadock.core._rich_ import repr_rich

from datadock.core._xml_ import xml_namespaces

from datadock.src._constants import IntString


test_live_xpath = (
    ".//*[local-name()='testOrLive' or local-name()='liveTestFlag']"
    "/text()"
)

street1_xpath = (
    "//*[local-name()='primaryIssuer']/*[local-name()='issuerAddress']/*[local-name()='street1']/text()"
    " | //*[local-name()='filingManager']/*[local-name()='address']/*[local-name()='street1']/text()"
    " | //*[local-name()='offeringData']/*[local-name()='salesCompensationList']/*[local-name()='recipient']"
    "/*[local-name()='recipientAddress']/*[local-name()='street1']/text()"
)

street2_xpath = (
    "//*[local-name()='primaryIssuer']/*[local-name()='issuerAddress']/*[local-name()='street2']/text()"
    " | //*[local-name()='filingManager']/*[local-name()='address']/*[local-name()='street2']/text()"
    " | //*[local-name()='offeringData']/*[local-name()='salesCompensationList']/*[local-name()='recipient']"
    "/*[local-name()='recipientAddress']/*[local-name()='street2']/text()"
)

city_xpath = (
    "//*[local-name()='primaryIssuer']/*[local-name()='issuerAddress']/*[local-name()='city']/text()"
    " | //*[local-name()='filingManager']/*[local-name()='address']/*[local-name()='city']/text()"
    " | //*[local-name()='offeringData']/*[local-name()='salesCompensationList']/*[local-name()='recipient']"
    "/*[local-name()='recipientAddress']/*[local-name()='city']/text()"
)

state_or_country_xpath = (
    "//*[local-name()='primaryIssuer']/*[local-name()='issuerAddress']/*[local-name()='stateOrCountry']/text()"
    " | //*[local-name()='filingManager']/*[local-name()='address']/*[local-name()='stateOrCountry']/text()"
    " | //*[local-name()='offeringData']/*[local-name()='salesCompensationList']/*[local-name()='recipient']"
    "/*[local-name()='recipientAddress']/*[local-name()='stateOrCountry']/text()"
)

state_or_country_desc_xpath = (
    "//*[local-name()='primaryIssuer']/*[local-name()='issuerAddress']/*[local-name()='stateOrCountryDescription']/text()"
    " | //*[local-name()='offeringData']/*[local-name()='salesCompensationList']/*[local-name()='recipient']"
    "/*[local-name()='recipientAddress']/*[local-name()='stateOrCountryDescription']/text()"
)

zipcode_xpath = (
    "//*[local-name()='primaryIssuer']/*[local-name()='issuerAddress']/*[local-name()='zipCode']/text()"
    " | //*[local-name()='filingManager']/*[local-name()='address']/*[local-name()='zipCode']/text()"
    " | //*[local-name()='offeringData']/*[local-name()='salesCompensationList']/*[local-name()='recipient']"
    "/*[local-name()='recipientAddress']/*[local-name()='zipCode']/text()"
)

signature_name_xpath = (
    "//*[local-name()='offeringData']/*[local-name()='signatureBlock']"
    "/*[local-name()='signature']/*[local-name()='signatureName']/text()"
    " | //*[local-name()='signatureBlock']/*[local-name()='name']/text()"
)

signature_signer_xpath = (
    "//*[local-name()='offeringData']/*[local-name()='signatureBlock']"
    "/*[local-name()='signature']/*[local-name()='nameOfSigner']/text()"
    " | //*[local-name()='signatureBlock']/*[local-name()='signature']/text()"
)

signature_title_xpath = (
    "//*[local-name()='offeringData']/*[local-name()='signatureBlock']"
    "/*[local-name()='signature']/*[local-name()='signatureTitle']/text()"
    " | //*[local-name()='signatureBlock']/*[local-name()='title']/text()"
)

signature_date_xpath = (
    "//*[local-name()='offeringData']/*[local-name()='signatureBlock']"
    "/*[local-name()='signature']/*[local-name()='signatureDate']/text()"
    " | //*[local-name()='signatureBlock']/*[local-name()='signatureDate']/text()"
)

issuer_size_xpath = (
    "//*[local-name()='offeringData']/*[local-name()='issuerSize']"
    "/*[local-name()='aggregateNetAssetValueRange']/text()"
    " | //*[local-name()='offeringData']/*[local-name()='issuerSize']"
    "/*[local-name()='revenueRange']/text()"
)


def get_text_or_default(base_element: etree.Element, xpath: str, default: str = "Not Available") -> str:
    """
    Retrieves the text content from an XML element using the provided XPath expression,
    returning a default value if no content is found.

    Parameters:
    -----------
    base_element : etree.Element
        The base XML element to search within using the XPath expression.
    xpath : str
        The XPath expression used to locate the desired text content within the XML element.
    default : str, optional
        The default value to return if no matching content is found. The default is "Not Available".

    Returns:
    --------
    str
        The text content found by the XPath expression, or the default value if no content is found.

    Example:
    --------
    >>> get_text_or_default(xml_element, "//name", "Unknown")
    'John Doe'

    This function performs an XPath search on the provided XML element and returns the
    first matching result. If no result is found, it returns the default value.
    """
    result = base_element.xpath(xpath, namespaces=xml_namespaces)
    return result[0] if result else default


class BusinessCombinationTransaction(BaseModel):
    """
    Represents a business combination transaction, typically in the context of SEC filings 
    or financial transactions.

    Attributes:
    -----------
    is_business_combination : str
        A string indicating whether the transaction is considered a business combination.
    clarification_of_response : Optional[str]
        An optional clarification or explanation regarding the response, if applicable.
    """
    is_business_combination: str
    clarification_of_response: Optional[str]


class OfferingSalesAmounts(BaseModel):
    """
    A class representing the total offering amount, total amount sold, total remaining, and clarification of response.

    Attributes:
    total_offering_amount: Optional[str]
        The total offering amount.
    total_amount_sold: Optional[str]
        The total amount sold.
    total_remaining: Optional[str]
        The total remaining.
    clarification_of_response: Optional[str]
        The clarification of response.
    """

    total_offering_amount: Optional[str]
    total_amount_sold: Optional[str]
    total_remaining: Optional[str]
    clarification_of_response: Optional[str]


class Investors(BaseModel):
    """
    A class representing investors in a SEC filing.

    Attributes:
    has_non_accredited_investors (str): A string indicating whether the offering has non-accredited investors.
    num_non_accredited_investors (str): A string representing the number of non-accredited investors.
    total_already_invested (str): An object representing the total amount already invested.
    """

    has_non_accredited_investors: str
    num_non_accredited_investors: str
    total_already_invested: str


class SalesCommissionFindersFees(BaseModel):
    """
    A class representing sales commission and finders fees, along with clarification of response.

    Attributes:
    sales_commission (str): The sales commission details.
    finders_fees (str): The finders fees details.
    clarification_of_response (Optional[str]): Clarification of the response, if any.
    """

    sales_commission: Optional[str]
    finders_fees: Optional[str]
    clarification_of_response: Optional[str]


class InvestmentFundInfo(BaseModel):
    """
    Represents information about an investment fund, including its type and regulatory classification.

    Attributes:
    -----------
    investment_fund_type : str, optional
        The type of investment fund (e.g., mutual fund, hedge fund, etc.).
    is_40_act : str, optional
        A string indicating whether the fund is subject to the Investment Company Act of 1940 (Yes/No).
    """
    investment_fund_type: str = None
    is_40_act: str = None


class IndustryGroup(BaseModel):
    """
    Represents an industry group classification.

    Attributes:
    -----------
    industry_group_type : str
        The type or name of the industry group (e.g., Technology, Healthcare, etc.).
    """
    industry_group_type: str


class UseOfProceeds(BaseModel):
    """
    A class representing the use of proceeds in a SEC filing.

    Attributes:
    gross_proceeds_used (str): The gross proceeds used in the SEC filing.
    is_estimate (str): Indicates whether the gross proceeds used is an estimate.
    clarification_of_response (Optional[str]): Clarification of the response provided.
    """

    gross_proceeds_used: str = None
    is_estimate: str = None
    clarification_of_response: Optional[str]


class SecurityTypes(BaseModel):
    """
    A class representing the types of securities offered in the offering.

    Attributes:
    equity (str): The amount of equity-type securities offered.
    debt (str): The amount of debt-type securities offered.
    options (str): The amount of options-type securities offered.
    security_acquire (str): The amount of security-to-be-acquired-type securities offered.
    pooled_investment (str): The amount of pooled-investment-fund-type securities offered.
    tenant_security (str): The amount of tenant-in-common-securities offered.
    mineral_security (str): The amount of mineral-property-securities offered.
    other (str): The amount of other-type securities offered.
    other_description (str): The description of other-type securities offered.
    """
    equity: str = None
    debt: str = None
    options: str = None
    security_acquire: str = None
    pooled_investment: str = None
    tenant_security: str = None
    mineral_security: str = None
    other: str = None
    other_description: str = None


class Signature(BaseModel):
    """
    A class representing a signature in a filing schema.

    Attributes
    ----------
    signature_name : str
        The name of the person signing the document.
    name_of_signer : str
        The full name of the person signing the document.
    title : Optional[str]
        The title of the person signing the document.
    date : Optional[str]
        The date of the signature.

    Methods
    -------
    None
    """
    signature_name: str = None
    name_of_signer: str = None
    title: Optional[str] = None
    date: Optional[str] = None


class FilingSchema(BaseModel):
    """
    A class representing a filing schema.

    Attributes
    ----------
    filing_schema : str
        The version of the filing schema.
    submission_type : str
        The type of submission.
    test_or_live : str
        Whether the submission is for testing or live data.

    Methods
    -------
    from_xml(cls, schema_el: Tag)
        A class method to create an instance of FilingSchema from an XML element.

    """

    filing_schema: str = None
    submission_type: str = None
    test_or_live: str = None

    @classmethod
    def from_xml(cls, schema_el: Tag) -> "FilingSchema":
        """
        Create an instance of FilingSchema from an XML element.

        Parameters
        ----------
        schema_el : Tag
            The XML element representing the filing schema.

        Returns
        -------
        FilingSchema
            An instance of FilingSchema created from the XML element.

        """
        return cls(
            filing_schema=get_text_or_default(schema_el, "//*[local-name()='schemaVersion']/text()"),
            submission_type=get_text_or_default(schema_el, "//*[local-name()='submissionType']/text()"),
            test_or_live=get_text_or_default(schema_el, test_live_xpath)
        )


class Flags(BaseModel):
    """
    A class representing the flags in a filing schema.

    Attributes
    ----------
    confirm_copy_flag : str
        A flag indicating whether the copy is confirming.
    return_copy_flag : str
        A flag indicating whether the copy is a return copy.
    override_internet_flag : str
        A flag indicating whether the internet flag should be overridden.

    Methods
    -------
    from_xml(cls, flags_el: Tag)
        A class method to create an instance of Flags from an XML element.

    """
    confirm_copy_flag: str = None
    return_copy_flag: str = None
    override_internet_flag: str = None

    @classmethod
    def from_xml(cls, flags_el: Tag) -> "Flags":
        """
        Create an instance of Flags from an XML element.

        Parameters
        ----------
        flags_el : Tag
            The XML element representing the flags.

        Returns
        -------
        Flags
            An instance of Flags created from the XML element.

        """
        return cls(
            confirm_copy_flag=get_text_or_default(flags_el, "//*[local-name()='flags']/*[local-name()='confirmingCopyFlag']/text()"),
            return_copy_flag=get_text_or_default(flags_el, "//*[local-name()='flags']/*[local-name()='returnCopyFlag']/text()"),
            override_internet_flag=get_text_or_default(flags_el, "//*[local-name()='flags']/*[local-name()='overrideInternetFlag']/text()")
        )


class Address(BaseModel):
    """
    A class representing an address.

    Attributes
    ----------
    street1 : str
        The first line of the street address.
    street2 : str
        The second line of the street address.
    city : str
        The city of the address.
    state_or_country : str
        The state or country of the address.
    state_or_country_description : str
        The description of the state or country.
    zipcode : str
        The zipcode of the address.

    Methods
    -------
    empty : property
        Returns True if the address is empty (all fields are None or empty), False otherwise.
    __str__ : method
        Returns a string representation of the address in the format "street1\nstreet2\ncity, state_or_country zipcode".
    __repr__ : method
        Returns a string representation of the address in the format "Address(street1='...', street2='...', city='...', zipcode='...', state_or_country='...' or '...')".
    """

    street1: str = None
    street2: str = None
    city: str = None
    state_or_country: str = None
    state_or_country_description: str = None
    zipcode: str = None

    @property
    def empty(self) -> bool:
        return not self.street1 and not self.street2 and not self.city and not self.state_or_country and not self.zipcode

    def __str__(self):
        if not self.street1:
            return ""
        address_format = "{street1}\n"
        if self.street2:
            address_format += "{street2}\n"
        address_format += "{city}, {state_or_country} {zipcode}"

        return address_format.format(
            street1=self.street1,
            street2=self.street2,
            city=self.city,
            state_or_country=self.state_or_country,
            zipcode=self.zipcode or ""
        )

    def __repr__(self):
        return (f'Address(street1="{self.street1 or ""}", street2="{self.street2 or ""}", city="{self.city or ""}",'
                f'zipcode="{self.zipcode or ""}", state_or_country="{self.state_or_country}" or "{self.state_or_country_description}")'
                )


class YearOfInc(BaseModel):
    """
    A class representing the year of incorporation of an issuer.

    Attributes:
    year_of_inc (str): The type of year of incorporation, either 'withinFiveYears' or 'overFiveYears'.
    year_of_inc_value (str): The value of the year of incorporation, if applicable.
    """

    year_of_inc: str = None
    year_of_inc_value: str = None

    @classmethod
    def from_xml(cls, year_of_inc_el: Tag) -> "YearOfInc":
        """
        Parses the XML element representing the year of incorporation and returns a YearOfInc object.

        Parameters:
        year_of_inc_el (Tag): The XML element representing the year of incorporation.

        Returns:
        YearOfInc: An instance of the YearOfInc class representing the parsed year of incorporation.
        """

        year_of_inc_var = None
        year_of_inc_value = None

        for child_node in year_of_inc_el.xpath("//*[local-name()='primaryIssuer']/*[local-name()='yearOfInc']"):
            for child in child_node:
                if child.tag in ["withinFiveYears", "overFiveYears"]:
                    year_of_inc_var = child.tag
                    if child.tag == "withinFiveYears" and child.text == "true":
                        year_of_inc_value = get_text_or_default(child_node, "./value/text()")

        return cls(
            year_of_inc=str(year_of_inc_var),
            year_of_inc_value=str(year_of_inc_value),
        )


class Issuer(BaseModel):
    """
    Represents an issuer in an SEC filing.

    Attributes:
    cik (IntString): Central Index Key (CIK) of the issuer.
    entity_name (str): Name of the issuer.
    entity_type (str): Type of the issuer.
    primary_address (Address): Address of the issuer.
    phone_number (str): Phone number of the issuer.
    edgar_previous_names (str): Previous names of the issuer as reported in EDGAR.
    issuer_previous_names (str): Previous names of the issuer.
    jurisdiction (str): Jurisdiction of incorporation of the issuer.
    entity_other_types_desc (str): Description of other types of the issuer.
    year_of_incorporation (YearOfInc): Year of incorporation of the issuer.
    """

    cik: IntString = None
    entity_name: str = None
    entity_type: str = None
    primary_address: Address
    phone_number: str = None
    edgar_previous_names: str = None
    issuer_previous_names: str = None
    jurisdiction: str = None
    entity_other_types_desc: str = None
    year_of_incorporation: YearOfInc = None

    @classmethod
    def from_xml(cls, issuer_el: Tag) -> "Issuer":
        """
        Parses an XML element representing an issuer and returns an Issuer object.

        Parameters:
        issuer_el (Tag): XML element representing an issuer.

        Returns:
        Issuer: Issuer object parsed from the XML element.
        """

        # address
        address = Address(
            street1=get_text_or_default(issuer_el, street1_xpath),
            street2=get_text_or_default(issuer_el, street2_xpath),
            city=get_text_or_default(issuer_el, city_xpath),
            state_or_country=get_text_or_default(issuer_el, state_or_country_xpath),
            state_or_country_description=get_text_or_default(issuer_el, state_or_country_desc_xpath),
            zipcode=get_text_or_default(issuer_el, zipcode_xpath)
        )

        # edgar previous names
        if issuer_el.xpath("//*[local-name()='primaryIssuer']/*[local-name()='edgarPreviousNameList']/*[local-name()='previousName']/text()"):
            edgar_previous_names = ", ".join(issuer_el.xpath("//*[local-name()='primaryIssuer']/*[local-name()='edgarPreviousNameList']/*[local-name()='previousName']/text()", namespaces=xml_namespaces))
        else:
            edgar_previous_names = get_text_or_default(issuer_el, "//*[local-name()='primaryIssuer']/*[local-name()='edgarPreviousNameList']/*[local-name()='value']/text()")

        # year of incorporation
        year_of_inc_el = YearOfInc.from_xml(issuer_el)

        return cls(
            cik=get_text_or_default(issuer_el, "//*[local-name()='primaryIssuer']/*[local-name()='cik']/text()"),
            entity_name=get_text_or_default(issuer_el, "//*[local-name()='primaryIssuer']/*[local-name()='entityName']/text()"),
            phone_number=get_text_or_default(issuer_el, "//*[local-name()='primaryIssuer']/*[local-name()='issuerPhoneNumber']/text()"),
            entity_type=get_text_or_default(issuer_el, "//*[local-name()='primaryIssuer']/*[local-name()='entityType']/text()"),
            entity_other_types_desc=get_text_or_default(issuer_el, "//*[local-name()='primaryIssuer']/*[local-name()='entityTypeOtherDesc']/text()"),
            primary_address=address,
            edgar_previous_names=edgar_previous_names or "Not Available",
            jurisdiction=get_text_or_default(issuer_el, "//*[local-name()='primaryIssuer']/*[local-name()='jurisdictionOfInc']/text()"),
            issuer_previous_names=get_text_or_default(issuer_el, "//*[local-name()='primaryIssuer']/*[local-name()='issuerPreviousNameList']/*[local-name()='value']/text()"),
            year_of_incorporation=year_of_inc_el,
        )

    def __rich__(self):
        """
        Returns a rich representation of the Issuer object.
        """
        table = Table("issuer", "entity type")
        table.add_row(self.entity_name, self.entity_type)
        return Group(table)

    def __repr__(self):
        """
        Returns a string representation of the Issuer object.
        """
        return repr_rich(self.__rich__())


class FileManager(BaseModel):
    """
    A class representing a file manager in an SEC filing.

    Attributes:
    name (str): The name of the file manager.
    address (Address): The address of the file manager.
    amendment (str): Indicates if the filing is an amendment.
    amendment_num (str): The number of the amendment.
    amendment_type (str): The type of the amendment.

    Methods:
    from_xml(cls, manager_el: Tag):
        Parses an XML element representing a file manager and returns a FileManager object.
    """

    name: str
    address: Address
    amendment: str = None
    amendment_num: str = None
    amendment_type: str = None

    @classmethod
    def from_xml(cls, manager_el: Tag) -> "FileManager":
        """
        Parses an XML element representing a file manager and returns a FileManager object.

        Parameters:
        manager_el (Tag): XML element representing a file manager.

        Returns:
        FileManager: FileManager object parsed from the XML element.
        """

        # address
        address = Address(
            street1=get_text_or_default(manager_el, street1_xpath),
            street2=get_text_or_default(manager_el, street2_xpath),
            city=get_text_or_default(manager_el, city_xpath),
            state_or_country=get_text_or_default(manager_el, state_or_country_xpath),
            zipcode=get_text_or_default(manager_el, zipcode_xpath)
        )

        return cls(
            name=get_text_or_default(manager_el, "//*[local-name()='filingManager']/*[local-name()='name']/text()"),
            address=address,
            amendment=get_text_or_default(manager_el, "//*[local-name()='isAmendment']/text()"),
            amendment_num=get_text_or_default(manager_el, "//*[local-name()='amendmentNo']/text()"),
            amendment_type=get_text_or_default(manager_el, "//*[local-name()='amendmentInfo']/*[local-name()='amendmentType']/text()")
        )


class FileReport(BaseModel):
    """
    A class representing a file report.

    Attributes:
    report_type (str): The type of the report.
    form_13 (str): The form 13F file number.
    crd (str): The CRD number.
    sec_file_num (str): The SEC file number.
    provide_info (str): Information provided for instruction 5.
    """

    report_type: str = None
    form_13: str = None
    crd: str = None
    sec_file_num: str = None
    provide_info: str = None

    @classmethod
    def from_xml(cls, report_el: Tag) -> "FileReport":
        """
        Constructs a FileReport object from XML data.

        Parameters:
        report_el (Tag): The XML element containing the report data.

        Returns:
        FileReport: A FileReport object constructed from the XML data.
        """

        return cls(
            report_type=get_text_or_default(report_el, "//*[local-name()='reportType']/text()"),
            form_13=get_text_or_default(report_el, "//*[local-name()='form13FFileNumber']/text()"),
            crd=get_text_or_default(report_el, "//*[local-name()='crdNumber']/text()"),
            sec_file_num=get_text_or_default(report_el, "//*[local-name()='secFileNumber']/text()"),
            provide_info=get_text_or_default(report_el, "//*[local-name()='provideInfoForInstruction5']/text()"),
        )


class Person:
    """
    Represents an individual person with detailed address and relationship information.

    Attributes:
    -----------
    first_name : str
        The first name of the person.
    last_name : str
        The last name of the person.
    street1 : str
        The first line of the person's street address.
    street2 : str
        The second line of the person's street address (if applicable).
    city : str
        The city in which the person resides.
    state_or_country : str
        The state or country where the person resides.
    state_or_country_description : str
        A description of the state or country (e.g., state code or country name).
    zip_code : str
        The zip code associated with the person's address.
    relationships : str, optional
        A description of the person's relationships (if applicable).
    relationship_clarifications : str, optional
        Clarifications or details related to the person's relationships (if applicable).

    Methods:
    --------
    from_xml(person_el: Tag) -> Person:
        Class method to create a `Person` instance from an XML element.
    __str__() -> str:
        Returns a string representation of the person, displaying the full name.
    __repr__() -> str:
        Returns a more compact string representation of the person, displaying first and last name.
    """
    def __init__(self,
                 first_name: str,
                 last_name: str,
                 street1: str,
                 street2: str,
                 city: str,
                 state_or_country: str,
                 state_or_country_description: str,
                 zip_code: str,
                 relationships: str = None,
                 relationship_clarifications: str = None) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.street1 = street1
        self.street2 = street2
        self.city = city
        self.state_or_country = state_or_country
        self.state_or_country_description = state_or_country_description
        self.zip_code = zip_code
        self.relationships = relationships
        self.relationship_clarifications = relationship_clarifications

    @classmethod
    def from_xml(cls, person_el: Tag) -> "Person":
        """
        Constructs a Person object from XML data.

        Parameters:
        person_el (Tag): The XML element containing the person data.

        Returns:
        Person: A Person object constructed from the XML data.
        """
        first_names = []
        last_names = []
        street1_addresses = []
        street2_addresses = []
        city_addresses = []
        state_or_country_addresses = []
        state_or_country_desc_addresses = []
        zip_code_addresses = []
        relationships = []
        relationship_clarifications = []

        for person in person_el.xpath("//relatedPersonsList/relatedPersonInfo"):
            first_name = get_text_or_default(person, "relatedPersonName/firstName/text()")
            last_name = get_text_or_default(person, "relatedPersonName/lastName/text()")
            addresses = Address(
                street1 = get_text_or_default(person, "relatedPersonAddress/street1/text()"),
                street2 = get_text_or_default(person, "relatedPersonAddress/street2/text()"),
                city = get_text_or_default(person, "relatedPersonAddress/city/text()"),
                state_or_country = get_text_or_default(person, "relatedPersonAddress/stateOrCountry/text()"),
                state_or_country_description = get_text_or_default(person, "relatedPersonAddress/stateOrCountryDescription/text()"),
                zipcode = get_text_or_default(person, "relatedPersonAddress/zipCode/text()")

            )
            relationship = get_text_or_default(person, "relatedPersonRelationshipList/relationship/text()")
            relationship_clarification = get_text_or_default(person, "relationshipClarification/text()")

            # Append values to temporary lists
            first_names.append(first_name or "")
            last_names.append(last_name or "")
            street1_addresses.append(addresses.street1 or "")
            street2_addresses.append(addresses.street2 or "")
            city_addresses.append(addresses.city or "")
            state_or_country_addresses.append(addresses.state_or_country or "")
            state_or_country_desc_addresses.append(addresses.state_or_country_description or "")
            zip_code_addresses.append(addresses.zipcode or "")
            relationships.append(relationship or "")
            relationship_clarifications.append(relationship_clarification or "")

        return cls(
            first_name=", ".join(first_names),
            last_name=", ".join(last_names),
            street1=", ".join(street1_addresses),
            street2=", ".join(street2_addresses),
            city=", ".join(city_addresses),
            state_or_country=", ".join(state_or_country_addresses),
            state_or_country_description=", ".join(state_or_country_desc_addresses),
            zip_code=", ".join(zip_code_addresses),
            relationships=", ".join(relationships),
            relationship_clarifications=", ".join(relationship_clarifications)
        )

    def __str__(self):
        return f"{self.first_name} {self.first_name}"

    def __repr__(self):
        return f"{self.first_name} {self.last_name}"


class Name:
    """
    A class representing a person's name.

    Attributes:
    first_name (str): The first name of the person.
    middle_name (str): The middle name of the person.
    last_name (str): The last name of the person.
    suffix (Optional[str]): The suffix of the person's name.
    """

    def __init__(self,
                 first_name: str,
                 middle_name: str,
                 last_name: str,
                 suffix:Optional[str]=None) -> None:
        """
        Constructs all the necessary attributes for the Name object.

        Parameters:
        first_name (str): The first name of the person.
        middle_name (str): The middle name of the person.
        last_name (str): The last name of the person.
        suffix (Optional[str]): The suffix of the person's name.
        """
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.suffix = suffix

    @property
    def full_name(self) -> str:
        """
        Returns the full name of the person, combining the first name, middle name, last name, and suffix.
        """
        return f"{self.first_name}{' ' + self.middle_name or ''} {self.last_name} {self.suffix or ''}".rstrip()

    def __str__(self):
        """
        Returns the full name of the person.
        """
        return self.full_name

    def __repr__(self):
        """
        Returns the full name of the person.
        """
        return self.full_name


class Filer:
    """
    A class representing a filer in a SEC filing.

    Attributes:
    cik (str): The Central Index Key (CIK) of the filer.
    entity_name (str): The name of the filer's entity.
    file_number (str): The file number assigned to the filer.
    """

    def __init__(self,
                 cik: str,
                 entity_name: str,
                 file_number: str
                 ) -> None:
        """
        Initializes a Filer object with the provided parameters.

        Parameters:
        cik (str): The Central Index Key (CIK) of the filer.
        entity_name (str): The name of the filer's entity.
        file_number (str): The file number assigned to the filer.
        """
        self.cik: str = cik
        self.entity_name: str = entity_name
        self.file_number: str = file_number

    def __str__(self):
        """
        Returns a string representation of the Filer object in the format "Entity Name (CIK)".

        Returns:
        str: The string representation of the Filer object.
        """
        return f"{self.entity_name} ({self.cik})"

    def __repr__(self):
        """
        Returns a string representation of the Filer object in the format "Entity Name (CIK)".

        Returns:
        str: The string representation of the Filer object.
        """
        return f"{self.entity_name} ({self.cik})"


class Contact:
    """
    A class representing a contact with name, phone number, and email.

    Attributes:
    name (str): The name of the contact.
    phone_number (str): The phone number of the contact.
    email (str): The email of the contact.
    """

    def __init__(self,
                 name: str,
                 phone_number: str,
                 email: str) -> None:
        """
        Initializes a Contact object with the provided parameters.

        Parameters:
        name (str): The name of the contact.
        phone_number (str): The phone number of the contact.
        email (str): The email of the contact.
        """
        self.name: str = name
        self.phone_number: str = phone_number
        self.email: str = email

    def __str__(self):
        """
        Returns a string representation of the Contact object in the format "Name (Phone Number) Email".

        Returns:
        str: The string representation of the Contact object.
        """
        return f"{self.name} ({self.phone_number}) {self.email}"

    def __repr__(self):
        """
        Returns a string representation of the Contact object in the format "Name (Phone Number) Email".

        Returns:
        str: The string representation of the Contact object.
        """
        return f"{self.name} ({self.phone_number}) {self.email}"


class FileIdentity(BaseModel):
    """
    A class representing the identity of a file in a SEC filing.

    Attributes:
    cik (str): The Central Index Key (CIK) of the file.
    ccc (str): The Committee on Capital Markets (CCC) number of the file.
    """

    cik: str
    ccc: str

    @classmethod
    def from_xml(cls, file_identity_el: Tag) -> "FileIdentity":
        """
        Constructs a FileIdentity object from the provided XML element.

        Parameters:
        file_identity_el (Tag): The XML element containing the file identity data.

        Returns:
        FileIdentity: A FileIdentity object with the extracted CIK and CCC values.
        """
        return cls(
            cik=get_text_or_default(file_identity_el, "//*[local-name()='filer']/*[local-name()='credentials']/*[local-name()='cik']/text()"),
            ccc=get_text_or_default(file_identity_el, "//*[local-name()='filer']/*[local-name()='credentials']/*[local-name()='ccc']/text()")
        )


class CalendarReport(BaseModel):
    """
    A class representing the calendar report in a SEC filing.

    Attributes:
    period_of_report (str): The period of the report.
    report_calendar_quarter (str): The calendar quarter of the report.
    """

    period_of_report: str
    report_calendar_quarter: str

    @classmethod
    def from_xml(cls, report_el: Tag) -> "CalendarReport":
        """
        Constructs a CalendarReport object from the provided XML element.

        Parameters:
        report_el (Tag): The XML element containing the calendar report data.

        Returns:
        CalendarReport: A CalendarReport object with the extracted period of report and report calendar quarter values.
        """
        return cls(
            period_of_report=get_text_or_default(report_el, "//*[local-name()='periodOfReport']/text()"),
            report_calendar_quarter=get_text_or_default(report_el, "//*[local-name()='reportCalendarOrQuarter']/text()")
        )


class SignatureIssuer(BaseModel):
    """
    Represents a signature issuer, including information about the authorized representative, 
    the issuer's name, and associated signatures.

    Attributes:
    -----------
    authorized_representative : str, optional
        The name of the authorized representative who signed on behalf of the issuer.
    issuer_name : str, optional
        The name of the entity (issuer) being represented.
    signatures : Signature, optional
        The signatures associated with the issuer, typically containing the actual signature data.
    """
    authorized_representative: str = None
    issuer_name: str = None
    signatures: Signature = None

    @classmethod
    def from_xml(cls, signature_block_tag: Tag) -> "SignatureIssuer":
        """
        Parses XML data and constructs a SignatureIssuer object.

        Parameters:
        signature_block_tag (Tag): The XML element containing the signature block data.

        Returns:
        SignatureIssuer: A SignatureIssuer object with the extracted signature, authorized representative, and issuer name.
        """
        signature = Signature(
            signature_name=get_text_or_default(signature_block_tag, signature_name_xpath),
            name_of_signer=get_text_or_default(signature_block_tag, "//*[local-name()='offeringData']/*[local-name()='signatureBlock']/*[local-name()='signature']/*[local-name()='nameOfSigner']/text()"),
            title=get_text_or_default(signature_block_tag, signature_title_xpath),
            date=get_text_or_default(signature_block_tag, signature_date_xpath)
        )

        return cls(
            signatures=signature,
            authorized_representative=get_text_or_default(signature_block_tag, "//*[local-name()='offeringData']/*[local-name()='signatureBlock']/*[local-name()='authorizedRepresentative']/text()"),
            issuer_name=get_text_or_default(signature_block_tag, "//*[local-name()='offeringData']/*[local-name()='signatureBlock']/*[local-name()='signature']/*[local-name()='issuerName']/text()"),
        )


class SignatureBlock(BaseModel):
    """
    This class represents the signature block in the SEC filing.

    Attributes:
    signatures (Signature): An instance of the Signature class representing the signature details.
    phone (Optional[str]): The phone number of the signer.
    city (Optional[str]): The city where the signer is located.
    state (Optional[str]): The state where the signer is located.

    Methods:
    from_xml(cls, signature_block_tag: Tag): A class method that creates an instance of SignatureBlock from the XML tag.
    """
    signatures: Signature = None
    phone: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None

    @classmethod
    def from_xml(cls, signature_block_tag: Tag) -> "SignatureBlock":
        """
        Creates an instance of SignatureBlock from the XML tag.

        Parameters:
        signature_block_tag (Tag): The XML tag containing the signature block information.

        Returns:
        SignatureBlock: An instance of SignatureBlock with the extracted information.
        """
        signature = Signature(
            signature_name=get_text_or_default(signature_block_tag, signature_name_xpath),
            name_of_signer=get_text_or_default(signature_block_tag, signature_signer_xpath),
            title=get_text_or_default(signature_block_tag, signature_title_xpath),
            date=get_text_or_default(signature_block_tag, signature_date_xpath)
        )
        return cls(
            signatures=signature,
            phone=get_text_or_default(signature_block_tag, "//*[local-name()='signatureBlock']/*[local-name()='phone']/text()"),
            city=get_text_or_default(signature_block_tag, "//*[local-name()='signatureBlock']/*[local-name()='city']/text()"),
            state=get_text_or_default(signature_block_tag, "//*[local-name()='signatureBlock']/*[local-name()='stateOrCountry']/text()"),
        )


class Form13HROtherManagersInfo(BaseModel):
    """
    Represents information about other managers in a Form 13H filing, including details such as
    sequence number, SEC file number, Form 13 number, and manager names.

    Attributes:
    -----------
    seq_num : str, optional
        The sequence number of the manager in the filing.
    sec_file_number : str, optional
        The SEC file number associated with the manager.
    form13_number : str, optional
        The Form 13 number associated with the manager.
    name : str, optional
        The name of the other manager.
    """
    seq_num: str = None
    sec_file_number: str = None
    form13_number: str = None
    name: str = None

    @classmethod
    def from_xml(cls, other_managers_el: Tag) -> "Form13HROtherManagersInfo":
        """
        Parses an XML element representing the 'otherManagers' section of a Form 13H filing and
        returns an instance of `Form13HROtherManagersInfo` populated with the extracted information.

        Parameters:
        -----------
        other_managers_el : Tag
            An XML element containing the other managers' data.

        Returns:
        --------
        Form13HROtherManagersInfo
            An instance of `Form13HROtherManagersInfo` with the extracted sequence number,
            SEC file number, Form 13 number, and manager names.
        """
        manager_seq = []
        manager_form13 = []
        manager_sec = []
        manager_names = []
        if other_managers_el.xpath("//*[local-name()='otherManagers2Info']/*[local-name()='otherManager2']"):
            for child_node in other_managers_el.xpath("//*[local-name()='otherManagers2Info']/*[local-name()='otherManager2']"):
                seq_num_val = get_text_or_default(child_node, "*[local-name()='sequenceNumber']/text()")
                form13_num = get_text_or_default(child_node, "*[local-name()='otherManager']/*[local-name()='form13FFileNumber']/text()")
                sec_file_num = get_text_or_default(child_node, "*[local-name()='otherManager']/*[local-name()='secFileNumber']/text()")
                name_val = get_text_or_default(child_node, "*[local-name()='otherManager']/*[local-name()='name']/text()")

                manager_form13.append(form13_num or "")
                manager_sec.append(sec_file_num or "")
                manager_names.append(name_val or "")
                manager_seq.append(seq_num_val or "")

        return cls(
            seq_num=", ".join(manager_seq) or "Not Available",
            form13_number=", ".join(manager_form13) or "Not Available",
            sec_file_number=", ".join(manager_sec) or "Not Available",
            name=", ".join(manager_names) or "Not Available"
        )


class Form13NTOtherManagersInfo(BaseModel):
    """
    Represents information about other managers in a Form 13N filing, including details such as
    CIK (Central Index Key), Form 13 number, and manager names.

    Attributes:
    -----------
    cik : str, optional
        The Central Index Key (CIK) of the other manager.
    form13_number : str, optional
        The Form 13 number associated with the manager.
    name : str, optional
        The name of the other manager.
    """
    cik: str = None
    form13_number: str = None
    name: str = None

    @classmethod
    def from_xml(cls, other_managers_el: Tag) -> "Form13NTOtherManagersInfo":
        """
        Parses an XML element representing the 'otherManagers' section of a Form 13N filing and 
        returns an instance of `Form13NTOtherManagersInfo` populated with the extracted information.

        Parameters:
        -----------
        other_managers_el : Tag
            An XML element containing the other managers' data.

        Returns:
        --------
        Form13NTOtherManagersInfo
            An instance of `Form13NTOtherManagersInfo` with the extracted CIK, 
            Form 13 number, and manager names.
        """
        manager_cik = []
        manager_form13 = []
        manager_names = []
        if other_managers_el.xpath("//*[local-name()='otherManagersInfo']/*[local-name()='otherManager']"):
            for child_node in other_managers_el.xpath("//*[local-name()='otherManagersInfo']/*[local-name()='otherManager']"):
                cik = get_text_or_default(child_node, "*[local-name()='cik']/text()")
                form13_num = get_text_or_default(child_node,"*[local-name()='form13FFileNumber']/text()")
                name_val = get_text_or_default(child_node,"*[local-name()='name']/text()")

                manager_form13.append(form13_num or "")
                manager_cik.append(cik or "")
                manager_names.append(name_val or "")

        return cls(
            cik=", ".join(manager_cik) or "Not Available",
            form13_number=", ".join(manager_form13) or "Not Available",
            name=", ".join(manager_names) or "Not Available"
        )


class SummaryPage(BaseModel):
    """
    This class represents the Summary Page data from an SEC filing.

    Attributes:
    other_managers: The count of other included managers.
    table_entry: The total table entry.
    table_value: The total table value.
    confidential: Indicates whether the confidential information is omitted.
    """

    other_managers: Optional[str] = None
    table_entry: Optional[str] = None
    table_value: Optional[str] = None
    confidential: Optional[str] = None

    @classmethod
    def from_xml(cls, summary_tag: Tag) -> "SummaryPage":
        """
        This method creates a SummaryPage object from the given XML tag.

        Parameters:
        summary_tag (Tag): The XML tag containing the summary page data.

        Returns:
        SummaryPage: A SummaryPage object with the extracted data.
        """

        return cls(
            other_managers=get_text_or_default(summary_tag, "//*[local-name()='summaryPage']/*[local-name()='otherIncludedManagersCount']/text()"),
            table_entry=get_text_or_default(summary_tag, "//*[local-name()='summaryPage']/*[local-name()='tableEntryTotal']/text()"),
            table_value=get_text_or_default(summary_tag, "//*[local-name()='summaryPage']/*[local-name()='tableValueTotal']/text()"),
            confidential=get_text_or_default(summary_tag, "//*[local-name()='summaryPage']/*[local-name()='isConfidentialOmitted']/text()")
        )


class SalesCompensationRecipient(BaseModel):
    """
    Represents information about a sales compensation recipient, including details such as name, CRD number,
    associated broker-dealer information, address, and solicitation data.

    Attributes:
    -----------
    name : str, optional
        The name of the compensation recipient.
    crd_name : str, optional
        The CRD number of the compensation recipient.
    associated_bd_name : str, optional
        The name of the associated broker-dealer.
    associated_bd_crd : str, optional
        The CRD number of the associated broker-dealer.
    street1 : str, optional
        The first line of the recipient's address.
    street2 : str, optional
        The second line of the recipient's address.
    city : str, optional
        The city of the recipient's address.
    state_or_country : str, optional
        The state or country of the recipient's address.
    state_or_country_desc : str, optional
        A description of the state or country of the recipient's address.
    zip_code : str, optional
        The ZIP code of the recipient's address.
    solicitation : str, optional
        The solicitation information for the recipient.
    """
    name: str = None
    crd_name: str = None
    associated_bd_name: str = None
    associated_bd_crd: str = None
    street1: str = None
    street2: str = None
    city: str = None
    state_or_country: str = None
    state_or_country_desc: str = None
    zip_code: str = None
    solicitation: str = None

    @classmethod
    def from_xml(cls,  recipient_tag: Tag) -> "SalesCompensationRecipient":
        """
        Parses an XML element representing a sales compensation recipient and
        returns an instance of `SalesCompensationRecipient` populated with the extracted information.

        Parameters:
        -----------
        recipient_tag : Tag
            An XML element containing the recipient's data.

        Returns:
        --------
        SalesCompensationRecipient
            An instance of `SalesCompensationRecipient` with the extracted name, CRD number,
            associated broker-dealer details, address, and solicitation information.
        """
        # Name and Crd can be "None"
        sales_names = []
        sales_crd_num = []
        sales_bd_name = []
        sales_bd_crd_num = []
        sales_street1_addresses = []
        sales_street2_addresses = []
        sales_city_addresses = []
        sales_state_or_country_addresses = []
        sales_state_or_country_desc_addresses = []
        sales_zip_code_addresses = []
        sales_solicitation_value = []

        if recipient_tag.xpath("//*[local-name()='offeringData']/*[local-name()='salesCompensationList']/*[local-name()='recipient']"):
            for recipient in recipient_tag.xpath("//*[local-name()='offeringData']/*[local-name()='salesCompensationList']/*[local-name()='recipient']"):
                re_names = get_text_or_default(recipient, "*[local-name()='recipientName']/text()")
                re_crd = get_text_or_default(recipient, "*[local-name()='recipientSCRNumber']/text()")
                re_bd_name = get_text_or_default(recipient, "*[local-name()='associatedBDName']/text()")
                re_bd_crd = get_text_or_default(recipient, "*[local-name()='associatedBDCRDNumber']/text()")

                addresses = Address(
                    street1=get_text_or_default(recipient, "*[local-name()='recipientAddress']/*[local-name()='street1']/text()"),
                    street2=get_text_or_default(recipient, "*[local-name()='recipientAddress']/*[local-name()='street2']/text()"),
                    city=get_text_or_default(recipient, "*[local-name()='recipientAddress']/*[local-name()='city']/text()"),
                    state_or_country=get_text_or_default(recipient, "*[local-name()='recipientAddress']/*[local-name()='stateOrCountry']/text()"),
                    state_or_country_description=get_text_or_default(recipient, "*[local-name()='recipientAddress']/*[local-name()='stateOrCountryDescription']/text()"),
                    zipcode=get_text_or_default(recipient, "*[local-name()='recipientAddress']/*[local-name()='zipCode']/text()")
                )
                solicitation_value = get_text_or_default(recipient, "*[local-name()='foreignSolicitation']/text()")

                sales_names.append(re_names or "")
                sales_crd_num.append(re_crd or "")
                sales_bd_name.append(re_bd_name or "")
                sales_bd_crd_num.append(re_bd_crd or "")
                sales_street1_addresses.append(addresses.street1 or "")
                sales_street2_addresses.append(addresses.street2 or "")
                sales_city_addresses.append(addresses.city or "")
                sales_state_or_country_addresses.append(addresses.state_or_country or "")
                sales_state_or_country_desc_addresses.append(addresses.state_or_country_description or "")
                sales_zip_code_addresses.append(addresses.zipcode or "")
                sales_solicitation_value.append(solicitation_value or "")

        return cls(
            name=", ".join(sales_names) or "Not Available",
            crd_name=", ".join(sales_crd_num) or "Not Available",
            associated_bd_name=", ".join(sales_bd_name) or "Not Available",
            associated_bd_crd=", ".join(sales_bd_crd_num) or "Not Available",
            street1=", ".join(sales_street1_addresses or ""),
            street2=", ".join(sales_street2_addresses or ""),
            city=", ".join(sales_city_addresses or ""),
            state_or_country=", ".join(sales_state_or_country_addresses or ""),
            state_or_country_desc=", ".join(sales_state_or_country_desc_addresses or ""),
            zip_code=", ".join(sales_zip_code_addresses or ""),
            solicitation=", ".join(sales_solicitation_value or "")
        )


class OfferingData:
    """
    Represents the offering data for a securities filing, including industry group, investment information,
    offering details, and associated financial data.

    Attributes:
        industry_group (IndustryGroup): The industry group associated with the offering.
        investment_fund (str): The type of investment fund involved in the offering, if applicable.
        is_40_act (str): Indicates whether the offering is subject to the 40 Act.
        revenue_range (str): The revenue range of the offering entity.
        federal_exemptions (str): Federal exemptions related to the offering.
        is_new (str): Whether the offering is new or an amendment.
        previous_accession_number (str): The accession number of the previous offering, if applicable.
        date_of_first_sale (str): The date of the first sale of securities in the offering.
        more_than_one_year (bool): Indicates if the offering will last more than one year.
        securities (SecurityTypes): Information about the types of securities being offered.
        business_combination_transaction (BusinessCombinationTransaction): Details of any business combination transaction.
        minimum_investment (str): The minimum investment required for participation in the offering.
        offering_sales_amounts (OfferingSalesAmounts): Financial information related to the sales amounts of the offering.
        investors (Investors): Information about the investors in the offering.
        sales_commission_finders_fees (SalesCommissionFindersFees): Details of the commissions and fees related to the offering.
        use_of_proceeds (UseOfProceeds): Information on how the proceeds from the offering will be used.
    """
    def __init__(self,
                 industry_group: IndustryGroup,
                 investment_fund: str = None,
                 is_40_act: str = None,
                 revenue_range: str = None,
                 federal_exemptions: str = None,
                 is_new: str = None,
                 previous_accession_number: str = None,
                 date_of_first_sale: str = None,
                 more_than_one_year: str = None,
                 securities: SecurityTypes = None,
                 business_combination_transaction: BusinessCombinationTransaction = None,
                 minimum_investment: str = None,
                 offering_sales_amounts: OfferingSalesAmounts = None,
                 investors: Investors = None,
                 sales_commission_finders_fees: SalesCommissionFindersFees = None,
                 use_of_proceeds: UseOfProceeds = None
    ) -> None:
        """
        Initializes the OfferingData object with the provided information.

        Args:
            industry_group (IndustryGroup): The industry group associated with the offering.
            investment_fund (str): The type of investment fund, if applicable.
            is_40_act (str): Indicates if the offering is subject to the 40 Act.
            revenue_range (str): The revenue range of the offering entity.
            federal_exemptions (str): Federal exemptions related to the offering.
            is_new (str): Indicates if the offering is a new notice or an amendment.
            previous_accession_number (str): The accession number of the previous offering, if applicable.
            date_of_first_sale (str): The date of the first sale of securities in the offering.
            more_than_one_year (bool): Whether the offering lasts more than one year.
            securities (SecurityTypes): Information on the types of securities offered.
            business_combination_transaction (BusinessCombinationTransaction): Business combination transaction details.
            minimum_investment (str): The minimum investment amount.
            offering_sales_amounts (OfferingSalesAmounts): Information on offering sales amounts.
            investors (Investors): Information on investors in the offering.
            sales_commission_finders_fees (SalesCommissionFindersFees): Details on commissions and fees.
            use_of_proceeds (UseOfProceeds): Information on how the offering's proceeds are used.
        """
        self.industry_group: IndustryGroup = industry_group
        self.investment_fund: str = investment_fund
        self.is_40_act: str = is_40_act
        self.revenue_range: str = revenue_range
        self.federal_exemptions: str = federal_exemptions
        self.is_new: str = is_new
        self.previous_accession = previous_accession_number
        self.date_of_first_sale: str = date_of_first_sale
        self.more_than_one_year: str = more_than_one_year
        self.security = securities
        self.business_combination_transaction: BusinessCombinationTransaction = business_combination_transaction
        self.minimum_investment = minimum_investment
        self.offering_sales_amounts = offering_sales_amounts
        self.investors: Investors = investors
        self.sales_commission_finders_fees: SalesCommissionFindersFees = sales_commission_finders_fees
        self.use_of_proceeds: UseOfProceeds = use_of_proceeds

    @classmethod
    def from_xml(cls, offering_data_el: Tag) -> "OfferingData":
        """
        Creates an OfferingData object by parsing the provided XML element.

        Args:
            offering_data_el (Tag): The XML element containing the offering data.

        Returns:
            OfferingData: The populated OfferingData object.
        """
        # industryGroup
        prev_accession_num = ""

        industry_group_type = get_text_or_default(offering_data_el, "//*[local-name()='offeringData']/*[local-name()='industryGroup']/*[local-name()='industryGroupType']/text()")
        industry_group = IndustryGroup(industry_group_type=industry_group_type)
        investment_fund_info_el = offering_data_el.xpath("//*[local-name()='offeringData']/*[local-name()='industryGroup']/*[local-name()='investmentFundInfo']/text()")

        if investment_fund_info_el:
            investment_fund_info = InvestmentFundInfo(
                investment_fund_type=get_text_or_default(offering_data_el, "//*[local-name()='offeringData']/*[local-name()='industryGroup']/*[local-name()='investmentFundInfo']/*[local-name()='investmentFundType']/text()"),
                is_40_act=get_text_or_default(offering_data_el, "//*[local-name()='offeringData']/*[local-name()='industryGroup']/*[local-name()='investmentFundInfo']/*[local-name()='is40Act']/text()")
            )
            investment_type = investment_fund_info.investment_fund_type
            is_40_act = investment_fund_info.is_40_act
        else:
            investment_type = "Not Available"
            is_40_act = "Not Available"

        revenue_range = get_text_or_default(offering_data_el, issuer_size_xpath)

        fed_exemptions_el = ", ".join(offering_data_el.xpath("//*[local-name()='offeringData']/*[local-name()='federalExemptionsExclusions']/*[local-name()='item']/text()"))

        # type of filing
        new_or_amendment_el = get_text_or_default(offering_data_el, "//offeringData/typeOfFiling/newOrAmendment/isAmendment/text()")
        if new_or_amendment_el == "true":
            new_or_amendment = "Amendment"
            prev_accession_num = get_text_or_default(offering_data_el, "//offeringData/typeOfFiling/newOrAmendment/previousAccessionNumber/text()")
        else:
            new_or_amendment = "New Notice"

        date_first_sale_el = offering_data_el.xpath("//offeringData/typeOfFiling/dateOfFirstSale/value")
        if date_first_sale_el:
            date_of_first_sale = get_text_or_default(offering_data_el, "//offeringData/typeOfFiling/dateOfFirstSale/value/text()")
        else:
            date_of_first_sale = get_text_or_default(offering_data_el, "//offeringData/typeOfFiling/dateOfFirstSale/yetToOccur/text()")

        # Duration of transaction
        duration_of_offering_el = get_text_or_default(offering_data_el, "//offeringData/durationOfOffering/moreThanOneYear/text()")

        # Type of security
        security = SecurityTypes(
            equity=get_text_or_default(offering_data_el, "//offeringData/typesOfSecuritiesOffered/isEquityType/text()"),
            pooled_investment=get_text_or_default(offering_data_el, "//offeringData/typesOfSecuritiesOffered/isPooledInvestmentFundType/text()"),
            debt=get_text_or_default(offering_data_el, "//offeringData/typesOfSecuritiesOffered/isDebtType/text()"),
            options=get_text_or_default(offering_data_el, "//offeringData/typesOfSecuritiesOffered/isOptionToAcquireType/text()"),
            security_acquire=get_text_or_default(offering_data_el, "//offeringData/typesOfSecuritiesOffered/isSecurityToBeAcquiredType/text()"),
            tenant_security=get_text_or_default(offering_data_el, "//offeringData/typesOfSecuritiesOffered/isTenantInCommonSecurities/text()"),
            mineral_security=get_text_or_default(offering_data_el, "//offeringData/typesOfSecuritiesOffered/isMineralPropertySecurities/text()"),
            other=get_text_or_default(offering_data_el, "//offeringData/typesOfSecuritiesOffered/isOtherType/text()"),
            other_description=get_text_or_default(offering_data_el, "//offeringData/typesOfSecuritiesOffered/descriptionOfOtherType/text()"),
        )

        # Businss combination
        business_combination_transaction = BusinessCombinationTransaction(
            is_business_combination=get_text_or_default(offering_data_el, "//offeringData/businessCombinationTransaction/isBusinessCombinationTransaction/text()"),
            clarification_of_response=get_text_or_default(offering_data_el, "//offeringData/businessCombinationTransaction/clarificationOfResponse/text()")
        )

        # Minimum investment
        minimum_investment = get_text_or_default(offering_data_el, "//offeringData/minimumInvestmentAccepted/text()")

        # Offering Sales Amount
        offering_sales_amounts = OfferingSalesAmounts(
            total_offering_amount=get_text_or_default(offering_data_el, "//offeringData/offeringSalesAmounts/totalOfferingAmount/text()"),
            total_amount_sold=get_text_or_default(offering_data_el, "//offeringData/offeringSalesAmounts/totalAmountSold/text()"),
            total_remaining=get_text_or_default(offering_data_el, "//offeringData/offeringSalesAmounts/totalRemaining/text()"),
            clarification_of_response=get_text_or_default(offering_data_el, "//offeringData/offeringSalesAmounts/clarificationOfResponse/text()")
        )

        # investors
        investors = Investors(
            has_non_accredited_investors=get_text_or_default(offering_data_el, "//offeringData/investors/hasNonAccreditedInvestors/text()"),
            num_non_accredited_investors=get_text_or_default(offering_data_el, "//offeringData/investors/numberNonAccreditedInvestors/text()"),
            total_already_invested=get_text_or_default(offering_data_el, "//offeringData/investors/totalNumberAlreadyInvested/text()")
        )

        # salesCommissionsFindersFees
        sales_commission_finders_fees = SalesCommissionFindersFees(
            sales_commission=get_text_or_default(offering_data_el, "//offeringData/salesCommissionsFindersFees/salesCommissions/dollarAmount/text()"),
            finders_fees=get_text_or_default(offering_data_el, "//offeringData/salesCommissionsFindersFees/findersFees/dollarAmount/text()"),
            clarification_of_response=get_text_or_default(offering_data_el, "//offeringData/salesCommissionsFindersFees/clarificationOfResponse/text()")
        )

        # useOfProceeds
        use_of_proceeds = UseOfProceeds(
            gross_proceeds_used=get_text_or_default(offering_data_el, "//offeringData/useOfProceeds/grossProceedsUsed/dollarAmount/text()"),
            is_estimate=get_text_or_default(offering_data_el, "//offeringData/useOfProceeds/grossProceedsUsed/isEstimate/text()"),
            clarification_of_response=get_text_or_default(offering_data_el, "//offeringData/useOfProceeds/clarificationOfResponse/text()")
        )

        return cls(
            industry_group=industry_group,
            investment_fund=investment_type, is_40_act=is_40_act,
            revenue_range=revenue_range,
            federal_exemptions=fed_exemptions_el,
            is_new=new_or_amendment,
            previous_accession_number=prev_accession_num or "Not Available",
            date_of_first_sale=date_of_first_sale,
            more_than_one_year=duration_of_offering_el,
            securities=security,
            business_combination_transaction=business_combination_transaction,
            minimum_investment=minimum_investment,
            offering_sales_amounts=offering_sales_amounts,
            investors=investors,
            sales_commission_finders_fees=sales_commission_finders_fees,
            use_of_proceeds=use_of_proceeds
        )

    def __rich__(self):
        base_info_table = Table("amount offered", "amount sold", "investors", "minimum investment")
        base_info_table.add_row(self.offering_sales_amounts.total_offering_amount, self.offering_sales_amounts.total_amount_sold,
                                self.investors.total_already_invested,self.minimum_investment or "")
        return Group(
            Panel.fit(base_info_table, title="Offering Info", title_align="left", box=box.SIMPLE)
        )

    def __repr__(self):
        return repr_rich(self.__rich__())
