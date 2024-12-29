from djangoprime.core.exception import BaseHTTPException
from djangoprime.enum import ResponseEnum


class PasswordInvalidException(BaseHTTPException):
    """
     Exception raised when a user with the provided password does not verify.
    """
    response_code = ResponseEnum.EXCEPTIONS.AUTHENTICATION.PASSWORD_NOT_VALID.response_key
    message = ResponseEnum.EXCEPTIONS.AUTHENTICATION.PASSWORD_NOT_VALID.value
