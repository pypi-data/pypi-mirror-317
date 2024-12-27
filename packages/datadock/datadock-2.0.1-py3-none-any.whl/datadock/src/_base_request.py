"""
Module: _base_request.py
==========================
BaseRequestAPI serves as the base for creating client APIs to interact with the SEC Edgar API
with methods for handling HTTP requests, constructing HTTP headers, joining URLs with the API base URL,
and logging response information.
"""

import json
from abc import ABC, abstractmethod
from typing import Union, Optional, Dict, List, Any

from requests import Response, Session, RequestException

from datadock.src.logger import CustomLogger
from datadock.src._errors import DataDockServerError, InvalidRequestMethodError, APIConnectionError
from datadock.src.utils import make_http_headers


http_headers = make_http_headers()


class BaseRequest(ABC):
    _VALID_HTTP_METHODS: set[str] = {"GET", "POST", "PUT", "DELETE"}

    # pylint: disable=too-few-public-methods
    def __init__(
            self,
            session: Optional[Session] = None,
            logger: Optional[CustomLogger] = None,
    ) -> None:
        """
        Initialize the BaseRequest class.

        :param session: Optional requests.Session object to be used for making HTTP requests.
        :param logger: Optional CustomLogger object for logging messages.
        """
        self._logger = logger or CustomLogger().logger
        self._session = session or Session()

    @abstractmethod
    def _fetch_document(self) -> Optional[str]:
        """Fetch the SEC document using the GET method."""
        pass

    def _request(
        self,
        method: str,
        url: str,
        data: Union[Dict[str, Any], List[Any], None] = None,
        params: Union[Dict[str, Any], None] = None,
        **kwargs,
    ) -> Union[str, Response]:
        """
        Make an HTTP request to the specified URL.

        :param method: The HTTP method to use for the request.
        :param url: The URL to make the request to.
        :param data: Optional data to send with the request.
        :param params: Optional parameters to include in the URL query string.
        :param kwargs: Additional keyword arguments to pass to the requests.Session.request method.

        :return: The response data as a string if the request is successful, otherwise the requests.Response object.

        :raises InvalidRequestMethodError: If the specified HTTP method is not valid.
        :raises DataDockServerError: If the server returns a client or server error status code.
        :raises APIConnectionError: If there is an error making the request.
        """
        if method.upper() not in self._VALID_HTTP_METHODS:
            error_message = (
                f"Invalid HTTP method. '{method}'. Supported methods are {', '.join(self._VALID_HTTP_METHODS)}"
            )
            self._logger.error(error_message)
            raise InvalidRequestMethodError(error_message)

        self._logger.debug(url)

        # Filtering params and data, then converting data to JSON
        params = (
            {key: value for key, value in params.items() if value is not None}
            if params
            else None
        )
        data = json.dumps(data) if data else None

        try:
            with self._session.request(
                method,
                url=url,
                headers=http_headers,
                timeout=10,
                params=params,
                data=data,
                **kwargs,
            ) as response:
                response_data = response.text
                self._logger.info("Response Status Code: %s", response.status_code)
                if 400 <= response.status_code <= 500:
                    error_message = f"Client error occurred: {response.status_code}"
                    self._logger.error(error_message)
                    raise DataDockServerError(
                        message=error_message, status_code=response.status_code
                    )
                # Handle server error
                elif 500 <= response.status_code <= 600:
                    error_message = f"Server error occurred: {response.status_code}"
                    self._logger.error(error_message)
                    raise DataDockServerError(
                        message=error_message, status_code=response.status_code
                    )

                return response_data
        except (RequestException, Exception) as error:
            # Extract status code if available from the exception
            self._logger.error("Unable to make a request Error %s", error)
            raise APIConnectionError(message=f"Unable to make a request Error {error}")
