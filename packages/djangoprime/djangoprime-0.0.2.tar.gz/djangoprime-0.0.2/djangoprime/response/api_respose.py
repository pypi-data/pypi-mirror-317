from typing import Any, Optional

from rest_framework.response import Response

from djangoprime.enum import ResponseKeyEnum


class APIResponse(Response):
    """
    Custom response class that extends Django's rest_framework Response.
    It formats the response data in a structured way, including optional fields
    such as a message, response code, and results.

    Attributes:
        message (Optional[str]): Custom message to include in the response.
        data (Any): The main data to be returned in the response.
        response_code (Optional): The custom response code to include in the response.
        status_code (int): The HTTP status code for the response. Default is 200 (OK).

    Methods:
        __init__: Initializes the APIResponse instance with custom formatted data.
    """

    def __init__(self, message: Optional[str] = None, data: Any = None, response_code=None, status_code: int = 200):
        """
        Initializes a custom response structure using the provided parameters.

        Args:
            message (Optional[str]): The message to include in the response, or None if not provided.
            data (Any): The main data to return in the response, or None if not provided.
            response_code (Optional): The custom response code to include, or None if not provided.
            status_code (int): The HTTP status code for the response (default is 200).

        """
        # Initialize the response data dictionary
        response_data = {}

        # Add the response code to the response data if provided
        if response_code is not None:
            response_data[ResponseKeyEnum.RESPONSE_CODE.response_key] = response_code

        # Add the message to the response data if provided
        if message is not None:
            response_data[ResponseKeyEnum.MESSAGE.response_key] = message

        # Add the main data (results) to the response data if provided
        if data is not None:
            response_data[ResponseKeyEnum.RESULTS.response_key] = data

        # Call the parent class constructor with the formatted data and the specified status code
        super().__init__(response_data, status=status_code)
