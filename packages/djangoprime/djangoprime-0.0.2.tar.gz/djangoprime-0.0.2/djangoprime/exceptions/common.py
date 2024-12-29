from rest_framework import status

from djangoprime.core.exception import BaseHTTPException
from djangoprime.enum import ResponseEnum


# Custom exceptions for handling invalid input errors
# Custom exceptions for handling invalid input errors
class InvalidInputException(BaseHTTPException):
    """
    Exception raised when the input provided by the user is invalid.
    The response code and message are derived from the ResponseEnum.
    """
    response_code = ResponseEnum.EXCEPTIONS.RESPONSE.INVALID_INPUT_ERROR.response_key
    message = ResponseEnum.EXCEPTIONS.RESPONSE.INVALID_INPUT_ERROR.value


class ValidationFailedException(BaseHTTPException):
    """
    Exception raised for validation failures in API requests.

    This exception indicates that the input data does not meet validation criteria.
    It provides a standardized response format, including a response code and message.
    """
    response_code = ResponseEnum.EXCEPTIONS.RESPONSE.VALIDATION_ERROR.response_key
    message = ResponseEnum.EXCEPTIONS.RESPONSE.VALIDATION_ERROR.value


class InvalidValueException(BaseHTTPException):
    """
    Exception raised when the user provides an invalid value.
    The response code and message are derived from the ResponseEnum.
    """
    response_code = ResponseEnum.EXCEPTIONS.RESPONSE.INVALID_VALUE_ERROR.response_key
    message = ResponseEnum.EXCEPTIONS.RESPONSE.INVALID_VALUE_ERROR.value


# Custom exceptions for handling not found errors
class NotFoundException(BaseHTTPException):
    """
    Exception raised when a resource is not found or a user does not have the necessary permissions.
    This exceptions is mapped to a 404 Not found HTTP status code.
    """
    response_code = ResponseEnum.EXCEPTIONS.RESPONSE.NOT_FOUND.response_key
    status_code = status.HTTP_404_NOT_FOUND
    message = ResponseEnum.EXCEPTIONS.RESPONSE.NOT_FOUND.value


# Custom exceptions for handling unsupported media type errors
class UnsupportedMediaTypeException(BaseHTTPException):
    """
    Exception raised when the media type of the request is unsupported.
    This exceptions is mapped to a 405 Method Not Allowed HTTP status code.
    """
    response_code = ResponseEnum.EXCEPTIONS.RESPONSE.UNSUPPORTED_MEDIA_TYPE.response_key
    status_code = status.HTTP_405_METHOD_NOT_ALLOWED
    message = ResponseEnum.EXCEPTIONS.RESPONSE.UNSUPPORTED_MEDIA_TYPE.value


class PydanticClassRequiredException(BaseHTTPException):
    response_code = "pydantic__class__required"
    status_code = status.HTTP_400_BAD_REQUEST
    message = "Pydantic class is required"
