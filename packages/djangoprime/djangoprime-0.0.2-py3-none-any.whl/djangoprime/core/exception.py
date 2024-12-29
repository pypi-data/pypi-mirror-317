from typing import Optional, Any

from rest_framework import status
from rest_framework.exceptions import APIException

from djangoprime.enum import ResponseEnum


class BaseHTTPException(APIException):
    """
    A custom base exception class that overrides Django Rest Framework's APIException.

    This class is used for handling custom HTTP exceptions with configurable status code,
    response code, and messages from the ResponseEnum.

    Attributes:
        status_code (int): HTTP status code for the exceptions. Default is 400 (Bad Request).
        response_code (str): Custom response code from the ResponseEnum.
        message (str): Custom error message from the ResponseEnum.
    """

    # Default HTTP status code set to 400 (Bad Request)
    status_code = status.HTTP_400_BAD_REQUEST

    # Default response code from the ResponseEnum for HTTP exceptions
    response_code = ResponseEnum.EXCEPTIONS.RESPONSE.HTTP_EXCEPTION.response_key

    # Default message from the ResponseEnum for HTTP exceptions
    message = ResponseEnum.EXCEPTIONS.RESPONSE.HTTP_EXCEPTION.value

    def __init__(self, detail: Optional[Any] = None, message: Optional[str] = None):
        """
        Initialize the BaseHTTPException with optional detail and message parameters.

        This constructor sets the detail and message attributes based on the provided
        arguments or defaults. It also calls the parent constructor of APIException
        with the appropriate detail and status code.

        Args:
            detail (Optional[Any]): A detailed error message to be included in the exception. Defaults to None.
            message (Optional[str]): A custom message for the exception. Defaults to None.
        """
        # If detail is provided, set it. Otherwise, use the custom message or default message.
        self.detail = detail if detail is not None else message or self.message

        # Set the message attribute to the provided message or the default message.
        self.message = message if message is not None else self.message

        # Call the parent class (APIException) constructor with the given detail and status code.
        super().__init__(detail=self.detail, code=self.status_code)
