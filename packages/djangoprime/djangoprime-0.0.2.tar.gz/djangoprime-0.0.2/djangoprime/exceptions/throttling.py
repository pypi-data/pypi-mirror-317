from rest_framework import status

from djangoprime.core.exception import BaseHTTPException
from djangoprime.enum import ResponseEnum


# Custom exceptions for handling rate limit exceeded errors
class RateLimitExceededException(BaseHTTPException):
    """
    Exception raised when the user exceeds the allowed rate limit for API requests.
    This is used to prevent abuse or excessive load on the server.
    """
    response_code = ResponseEnum.EXCEPTIONS.THROTTLING.RATE_LIMIT_EXCEEDED.response_key
    message = ResponseEnum.EXCEPTIONS.THROTTLING.RATE_LIMIT_EXCEEDED.value
    status_code = status.HTTP_429_TOO_MANY_REQUESTS


# Custom exceptions for handling temporary block errors
class TemporaryBlockException(BaseHTTPException):
    """
    Exception raised when a user is temporarily blocked from making requests.
    This may happen after multiple rate limit violations.
    """
    response_code = ResponseEnum.EXCEPTIONS.THROTTLING.TEMPORARY_BLOCK.response_key
    message = ResponseEnum.EXCEPTIONS.THROTTLING.TEMPORARY_BLOCK.value
    detail = "You have been temporarily blocked from making requests. Please try again later."
    status_code = status.HTTP_429_TOO_MANY_REQUESTS


# Custom exceptions for handling persistent block errors
class PersistentBlockException(BaseHTTPException):
    """
    Exception raised when a user is permanently blocked from making requests.
    This indicates a severe violation of usage policies.
    """
    response_code = ResponseEnum.EXCEPTIONS.THROTTLING.PERSISTENT_BLOCK.response_key
    message = ResponseEnum.EXCEPTIONS.THROTTLING.PERSISTENT_BLOCK.value
    detail = "Your account has been permanently blocked from making requests due to repeated violations."
    status_code = status.HTTP_403_FORBIDDEN


# Custom exceptions for handling reset time notifications
class RateLimitResetException(BaseHTTPException):
    """
    Exception raised when a user tries to make a request before the rate limit resets.
    This informs the user of the time remaining until they can make requests again.
    """
    response_code = ResponseEnum.EXCEPTIONS.THROTTLING.RATE_LIMIT_RESET.response_key
    message = ResponseEnum.EXCEPTIONS.THROTTLING.RATE_LIMIT_RESET.value
    detail = "You must wait before making additional requests. Rate limit will reset in X seconds."
    status_code = status.HTTP_429_TOO_MANY_REQUESTS


# Custom exceptions for unauthorized access attempts
class UnauthorizedAccessException(BaseHTTPException):
    """
    Exception raised when an unauthorized access attempt is detected.
    """
    response_code = ResponseEnum.EXCEPTIONS.THROTTLING.UNAUTHORIZED_ACCESS.response_key
    message = ResponseEnum.EXCEPTIONS.THROTTLING.UNAUTHORIZED_ACCESS.value
    detail = "Unauthorized access attempt detected."
    status_code = status.HTTP_401_UNAUTHORIZED


# Custom exceptions for suspicious activity detection
class SuspiciousActivityException(BaseHTTPException):
    """
    Exception raised when suspicious activity is detected.
    """
    response_code = ResponseEnum.EXCEPTIONS.THROTTLING.SUSPICIOUS_ACTIVITY.response_key
    message = ResponseEnum.EXCEPTIONS.THROTTLING.SUSPICIOUS_ACTIVITY.value
    detail = "Suspicious activity detected. Please contact support."
    status_code = status.HTTP_403_FORBIDDEN


# Custom exceptions for API key usage limits
class ApiKeyExceededException(BaseHTTPException):
    """
    Exception raised when an API key's usage limit has been exceeded.
    """
    response_code = ResponseEnum.EXCEPTIONS.THROTTLING.API_KEY_EXCEEDED.response_key
    message = ResponseEnum.EXCEPTIONS.THROTTLING.API_KEY_EXCEEDED.value
    detail = "API key usage limit exceeded."
    status_code = status.HTTP_429_TOO_MANY_REQUESTS


# Custom exceptions for daily request limits
class DailyLimitExceededException(BaseHTTPException):
    """
    Exception raised when the daily request limit has been exceeded.
    """
    response_code = ResponseEnum.EXCEPTIONS.THROTTLING.DAILY_LIMIT_EXCEEDED.response_key
    message = ResponseEnum.EXCEPTIONS.THROTTLING.DAILY_LIMIT_EXCEEDED.value
    detail = "Daily request limit exceeded."
    status_code = status.HTTP_429_TOO_MANY_REQUESTS


# Custom exceptions for maximum concurrent connections
class MaxConnectionsReachedException(BaseHTTPException):
    """
    Exception raised when the maximum number of concurrent connections has been reached.
    """
    response_code = ResponseEnum.EXCEPTIONS.THROTTLING.MAX_CONNECTIONS_REACHED.response_key
    message = ResponseEnum.EXCEPTIONS.THROTTLING.MAX_CONNECTIONS_REACHED.value
    detail = "Maximum number of concurrent connections reached."
    status_code = status.HTTP_429_TOO_MANY_REQUESTS


# Custom exceptions for active rate limiting warnings
class RateLimitingActiveException(BaseHTTPException):
    """
    Exception raised when rate limiting is currently active.
    """
    response_code = ResponseEnum.EXCEPTIONS.THROTTLING.RATE_LIMITING_ACTIVE.response_key
    message = ResponseEnum.EXCEPTIONS.THROTTLING.RATE_LIMITING_ACTIVE.value
    detail = "Rate limiting is currently active. Please slow down your requests."
    status_code = status.HTTP_429_TOO_MANY_REQUESTS


# Custom exceptions for active rate limiting warnings
class OperationInProgressException(BaseHTTPException):
    """
    Exception raised when a user attempts to perform an action while an operation is still in progress.
    This indicates that the request cannot be processed at this time, and the user should wait.
    """
    response_code = ResponseEnum.EXCEPTIONS.THROTTLING.OPERATION_IN_PROGRESS.response_key
    message = ResponseEnum.EXCEPTIONS.THROTTLING.OPERATION_IN_PROGRESS.value
    status_code = status.HTTP_429_TOO_MANY_REQUESTS
