"""
Module: config.py
======================
This module handles the sec identity or email from the .env file
"""

from decouple import config
from datadock.src._errors import IdentityError


def check_sec_identity() -> str:
    """
    Retrieve the SEC identity from the environment variable.

    This function retrieves the SEC identity from the 'SEC_IDENTITY' environment variable.
    If the variable is not set, it raises a ValueError.

    Returns:
    str: The SEC identity retrieved from the environment variable.

    Raises:
    ValueError: If the 'SEC_IDENTITY' environment variable is not set.
    """
    identity = config("SEC_IDENTITY", default=None, cast=str)

    if not identity:
        error_message = """
        The SEC identity is required but was not provided and the 'SEC_IDENTITY' environment variable is not set.
        Please set the 'SEC_IDENTITY' environment variable in your environment or provide the identity directly.
        """
        raise IdentityError(message=error_message)
    return identity
