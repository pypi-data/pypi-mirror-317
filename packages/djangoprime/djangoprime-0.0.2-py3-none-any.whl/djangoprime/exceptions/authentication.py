from rest_framework import status

from djangoprime.core.exception import BaseHTTPException
from djangoprime.enum import ResponseEnum


class AuthenticationFailedException(BaseHTTPException):
    """
    Exception raised when authentication fails.
    """
    response_code = ResponseEnum.EXCEPTIONS.AUTHENTICATION.AUTHENTICATION_FAILED.response_key
    message = ResponseEnum.EXCEPTIONS.AUTHENTICATION.AUTHENTICATION_FAILED.value


class NotAuthenticatedException(BaseHTTPException):
    """
    Exception raised when a user is not authenticated.
    """
    response_code = ResponseEnum.EXCEPTIONS.AUTHENTICATION.NOT_AUTHENTICATED.response_key
    status_code = status.HTTP_401_UNAUTHORIZED
    message = ResponseEnum.EXCEPTIONS.AUTHENTICATION.NOT_AUTHENTICATED.value


class AlreadyAuthenticatedException(BaseHTTPException):
    """
    Exception raised when a user is already authenticated.
    """
    response_code = ResponseEnum.EXCEPTIONS.AUTHENTICATION.ALREADY_AUTHENTICATED.response_key
    status_code = status.HTTP_401_UNAUTHORIZED
    message = ResponseEnum.EXCEPTIONS.AUTHENTICATION.ALREADY_AUTHENTICATED.value


class UnauthorizedUserException(BaseHTTPException):
    """
    Exception raised when a user is authenticated but not authorized to perform a specific action.
    """
    status_code = status.HTTP_401_UNAUTHORIZED
    response_code = ResponseEnum.EXCEPTIONS.AUTHENTICATION.UNAUTHORIZED_USER.response_key
    message = ResponseEnum.EXCEPTIONS.AUTHENTICATION.UNAUTHORIZED_USER.value


class AccountNotActiveException(BaseHTTPException):
    """
    Exception raised when a user is not active.
    """
    status_code = status.HTTP_401_UNAUTHORIZED
    response_code = ResponseEnum.EXCEPTIONS.AUTHENTICATION.ACCOUNT_NOT_ACTIVE.response_key
    message = ResponseEnum.EXCEPTIONS.AUTHENTICATION.ACCOUNT_NOT_ACTIVE.value


class AccountNotExistsException(BaseHTTPException):
    """
     Exception raised when a user with the provided credentials does not exist.
    """
    response_code = ResponseEnum.EXCEPTIONS.AUTHENTICATION.ACCOUNT_NOT_EXIST.response_key
    status_code = status.HTTP_404_NOT_FOUND
    message = ResponseEnum.EXCEPTIONS.AUTHENTICATION.ACCOUNT_NOT_EXIST.value


class AccountAlreadyExistsException(BaseHTTPException):
    """
     Exception raised when a user with the provided credentials already exists.
    """
    response_code = ResponseEnum.EXCEPTIONS.AUTHENTICATION.ACCOUNT_ALREADY_EXISTS.response_key
    message = ResponseEnum.EXCEPTIONS.AUTHENTICATION.ACCOUNT_ALREADY_EXISTS.value
    status_code = status.HTTP_409_CONFLICT
