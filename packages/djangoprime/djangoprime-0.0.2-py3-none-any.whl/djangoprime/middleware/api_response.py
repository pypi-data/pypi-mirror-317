import json

from djangoprime.enum import ResponseKeyEnum
from djangoprime.helpers.date_and_time import get_current_timestamp

# Set of accepted HTTP status codes for successful responses (O(1) lookups for efficiency)
RESPONSE_STATUS_CODES = {200, 201, 202}

# List of accepted media types for handling specific response formats
ACCEPTED_MEDIA_TYPES = [
    'text/html',
    'text/javascript',
    'image/png',
    'image/jpeg',
    'application/javascript',
]


class APIResponseMiddleware:
    """
    Middleware class for modifying API responses. This middleware ensures that all API responses
    are formatted correctly and uniformly before being sent to the client.

    The middleware checks the content type of the response, processes the response data, and ensures
    that the response is in the correct format (JSON) and includes the necessary fields such as
    response code, status code, message, and timestamp.

    Attributes:
        get_response: The function to get the response for the request.

    Methods:
        __call__: Processes the response data after the view is executed.
        _handle_exception_response: Formats responses when an exception occurs.
        _handle_success_response: Formats successful responses.
        _prepare_custom_response_data: Prepares the response data in a structured format.
        _extract_safe_value: Safely extracts values from the response data.
        _convert_to_json: Converts the response data to JSON format.
    """

    def __init__(self, get_response):
        """
        Initializes the APIResponseMiddleware with the provided response function.

        Args:
            get_response: The function to get the response for the request.
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Processes the response data after the view has executed. This method modifies the response
        based on its content type and whether it is a successful response or an error response.

        Args:
            request: The incoming HTTP request.

        Returns:
            response_data: The modified response data, which is either success or exception response.
        """
        response_data = self.get_response(request)

        try:
            # Extract the content type from the response headers or accepted media type
            content_type = response_data.headers.get('Content-Type', "")
            media_type = content_type.split(';')[0].strip()

            # If no content type is found, use the accepted media type
            if not media_type:
                accepted_media_type = response_data.accepted_media_type
                media_type = accepted_media_type.split(';')[0].strip()

            # If the response content type is one of the accepted media types, return the response unmodified
            if media_type in ACCEPTED_MEDIA_TYPES:
                return response_data

            # If the response contains an exception, handle it separately
            if response_data.exception:
                return self._handle_exception_response(response_data)

            # If the response contains data, format it as a success response
            if hasattr(response_data, 'data'):
                return self._handle_success_response(response_data)

            # Set the response content type to JSON if not otherwise set
            response_data['content-type'] = 'application/json'

        except Exception as e:
            # Log the error if there is an issue processing the response
            print(f"Error in APIResponseMiddleware: {e}")
            # Optionally log the error or handle it accordingly

        return response_data

    def _handle_exception_response(self, response_data):
        """
        Processes the response when an exception has occurred. This method formats the response
        to return a custom exception response structure.

        Args:
            response_data: The response data containing the exception.

        Returns:
            response_data: The response data with the formatted exception response.
        """
        status_code = response_data.status_code
        # Extract exception-specific data
        response_data.data = response_data.data.get(ResponseKeyEnum.CUSTOM_EXCEPTION.response_key)

        # Prepare the response data
        exception_response = self._prepare_custom_response_data(response_data)
        # Convert the response data to JSON format
        response_data.content = self._convert_to_json(exception_response)

        return response_data

    def _handle_success_response(self, response_data):
        """
        Processes the response when a successful operation occurs. This method formats the response
        to include the necessary fields such as status code, message, and results.

        Args:
            response_data: The response data containing the successful results.

        Returns:
            response_data: The response data with the formatted success response.
        """
        # Prepare the response data
        response_data.data = self._prepare_custom_response_data(response_data)
        # Convert the response data to JSON format
        response_data.content = self._convert_to_json(response_data.data)

        return response_data

    def _prepare_custom_response_data(self, response):
        """
        Prepares the custom response data structure by extracting necessary values and organizing them
        according to the required format.

        Args:
            response: The response data to be formatted.

        Returns:
            dict: The custom structured response data.
        """
        status_code = response.status_code

        # Determine whether the response is a success or error response based on status code
        context_response_code = (
            ResponseKeyEnum.SUCCESS.response_key
            if status_code in RESPONSE_STATUS_CODES
            else ResponseKeyEnum.ERRORS.response_key
        )

        # Safely extract values from the response data
        response_code = self._extract_safe_value(response.data, ResponseKeyEnum.RESPONSE_CODE.response_key, context_response_code)
        message = self._extract_safe_value(response.data, ResponseKeyEnum.MESSAGE.response_key, response.status_text)
        results_data = self._extract_safe_value(response.data, ResponseKeyEnum.RESULTS.response_key, response.data)

        # Prepare the structured response data
        return {
            ResponseKeyEnum.RESPONSE_CODE.response_key: response_code,
            ResponseKeyEnum.STATUS_CODE.response_key: status_code,
            ResponseKeyEnum.RESULTS.response_key: {
                context_response_code: {
                    ResponseKeyEnum.DETAIL.response_key: results_data
                }
            },
            ResponseKeyEnum.MESSAGE.response_key: message,
            ResponseKeyEnum.TIMESTAMP.response_key: get_current_timestamp()
        }

    def _extract_safe_value(self, data, key, default):
        """
        Extracts a value from a dictionary safely, returning the provided default value if the key is not found.

        Args:
            data (dict): The dictionary from which to extract the value.
            key (str): The key to look for in the dictionary.
            default: The value to return if the key is not found.

        Returns:
            The value associated with the key, or the default value if the key is not found.
        """
        return data.pop(key, default)

    def _convert_to_json(self, data):
        """
        Converts the data to a JSON string, handling non-serializable objects by using the default `str` function.

        Args:
            data: The data to be converted to JSON.

        Returns:
            str: The JSON representation of the data.
        """
        return json.dumps(data, default=str)
