from rest_framework import status

from djangoprime.core.exception import BaseHTTPException
from djangoprime.enum import ResponseEnum


# Custom exceptions for handling expired token errors
class ExpiredTokenException(BaseHTTPException):
    """
    Exception raised when a token has expired.
    This is used to indicate that the user needs to re-authenticate.
    """
    response_code = ResponseEnum.EXCEPTIONS.TOKEN.TOKEN_EXPIRED.response_key
    message = ResponseEnum.EXCEPTIONS.TOKEN.TOKEN_EXPIRED.value
    detail = "The token has expired. Please refresh your token or re-authenticate."
    status_code = status.HTTP_401_UNAUTHORIZED


# Custom exceptions for handling invalid token errors
class InvalidTokenException(BaseHTTPException):
    """
    Exception raised when a provided token is invalid.
    This typically occurs during authentication or authorization checks.
    """
    # Response code indicating that the token is not valid
    response_code = ResponseEnum.EXCEPTIONS.TOKEN.TOKEN_NOT_VALID.response_key
    message = ResponseEnum.EXCEPTIONS.TOKEN.TOKEN_NOT_VALID.value
    detail = "The provided token is either invalid or malformed. Please check and try again."
    status_code = status.HTTP_401_UNAUTHORIZED


# Custom exceptions for handling missing token errors
class MissingTokenException(BaseHTTPException):
    """
    Exception raised when a required token is missing from the request.
    This indicates that the request cannot be processed without the token.
    """
    response_code = ResponseEnum.EXCEPTIONS.TOKEN.TOKEN_MISSING.response_key
    message = ResponseEnum.EXCEPTIONS.TOKEN.TOKEN_MISSING.value
    detail = "The token is missing from the request. Please include a valid token."
    status_code = status.HTTP_401_UNAUTHORIZED


# Custom exceptions for handling token revocation errors
class RevokedTokenException(BaseHTTPException):
    """
    Exception raised when a token has been revoked and is no longer valid.
    This typically occurs when a token has been explicitly invalidated.
    """
    response_code = ResponseEnum.EXCEPTIONS.TOKEN.TOKEN_REVOKED.response_key
    message = ResponseEnum.EXCEPTIONS.TOKEN.TOKEN_REVOKED.value
    detail = "The token has been revoked and is no longer valid. Please request a new token."
    status_code = status.HTTP_401_UNAUTHORIZED
