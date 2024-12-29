from rest_framework.exceptions import APIException, NotAuthenticated
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework_simplejwt.exceptions import InvalidToken

from djangoprime.enum import ResponseKeyEnum
from djangoprime.exceptions import NotAuthenticatedException, InvalidTokenException


def exception_handler(exc, context):
    """
    Custom exception handler for REST framework that formats API exceptions.

    This function customizes how exceptions are handled and ensures that error responses
    are returned in a consistent and structured format, particularly for authentication-related
    errors such as InvalidToken and NotAuthenticated.

    Args:
        exc (Exception): The exception that was raised during the API request.
        context (dict): Context data for the exception, typically including the request and view.

    Returns:
        Response: A Response object with the formatted error message and status code.
    """

    # Call REST framework's default exception handler first to handle common exceptions
    response = drf_exception_handler(exc, context)

    # Handle InvalidToken exceptions specifically for JWT token-related errors
    if isinstance(exc, InvalidToken):
        details = getattr(exc, "detail", {})
        detail_message = {}

        # Safely extract 'messages' from the InvalidToken exception details
        messages = details.get('messages', [])
        if messages:
            # Assuming we only care about the first message in the list
            first_message = messages[0]

            # Convert ErrorDetail objects to strings and extract relevant details
            detail_message['token_class'] = str(first_message.get('token_class', 'AccessToken'))
            detail_message['token_type'] = str(first_message.get('token_type', 'access'))
            detail_message[ResponseKeyEnum.MESSAGE.response_key] = str(first_message.get('message', InvalidTokenException.message))
            detail_message[ResponseKeyEnum.RESPONSE_CODE.response_key] = InvalidTokenException.response_code
            detail_message[ResponseKeyEnum.INFO.response_key] = str(details.get('detail', 'Invalid token.')) or InvalidTokenException.detail

            # Return a custom Response object for InvalidToken with appropriate status
            return Response({
                ResponseKeyEnum.CUSTOM_EXCEPTION.name.lower(): detail_message
            }, status=401)  # HTTP 401 for unauthorized due to invalid token

    # Handle other API exceptions, particularly NotAuthenticated exceptions
    if isinstance(exc, APIException):
        # Check for NotAuthenticated exception, using the custom exception handler if needed
        if isinstance(exc, NotAuthenticated):
            response_code = NotAuthenticatedException.response_code
        else:
            # For general APIExceptions, fallback to the default response code or custom code if available
            response_code = getattr(exc, ResponseKeyEnum.RESPONSE_CODE.response_key, exc.default_code)

        # Extract the message from the exception, using default message if not provided
        message = getattr(exc, ResponseKeyEnum.MESSAGE.response_key, exc.default_detail)

        # Prepare the custom response data structure
        response_data = build_response_data(exc, response_code, message)

        if response is not None:
            # Attach the formatted response data to the response object
            response.data = response_data

        return response

    return response


def build_response_data(exc, response_code, message):
    """
    Build the structured response data for API exceptions.

    This function structures the exception data into a specific format, including the response code,
    message, and any additional details about the exception.

    Args:
        exc (Exception): The exception object that was raised.
        response_code (str): The response code associated with the exception (e.g., '401' for unauthorized).
        message (str): The error message associated with the exception.

    Returns:
        dict: The structured response data to be returned in the response.
    """
    return {
        ResponseKeyEnum.CUSTOM_EXCEPTION.name.lower(): {
            ResponseKeyEnum.RESPONSE_CODE.name.lower(): response_code,
            ResponseKeyEnum.MESSAGE.name.lower(): message,
            ResponseKeyEnum.RESULTS.name.lower(): exc.detail,  # Attach the exception details if available
        }
    }
