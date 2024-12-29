import requests
from uuid import UUID


def is_valid_uuid(value):
    """
    Validate if the given value is a valid UUID.

    This function attempts to create a UUID object from the provided value.
    If the value can be successfully converted to a UUID, it returns True.
    If a ValueError is raised, indicating that the value is not a valid UUID,
    it returns False.

    Args:
        value (str or UUID): The value to be validated as a UUID.

    Returns:
        bool: True if the value is a valid UUID, False otherwise.

    Example:
        >>> is_valid_uuid('123e4567-e89b-12d3-a456-426614174000')
        True

        >>> is_valid_uuid('invalid-uuid-string')
        False

        >>> is_valid_uuid(UUID('123e4567-e89b-12d3-a456-426614174000'))
        True

        >>> is_valid_uuid('')
        False
    """
    try:
        # Attempt to create a UUID object from the value.
        UUID(str(value))  # Convert the value to string and try to parse it as a UUID.
        return True  # The value is a valid UUID.
    except ValueError:
        return False  # The value is not a valid UUID.


def is_valid_url(url=None):
    """
    Validate if the given URL is reachable and returns a successful HTTP response.

    This function attempts to send a GET request to the specified URL and checks
    if the status code of the response is 200 (OK). If the URL is reachable and
    returns a successful response, the function returns True. If the URL is
    not reachable or the response is unsuccessful, it returns False.

    Args:
        url (str): The URL to be validated.

    Returns:
        bool: True if the URL is reachable and returns a status code of 200,
              False otherwise.

    Example:
        >>> is_valid_url('https://www.example.com')
        True

        >>> is_valid_url('https://invalid-url')
        False

        >>> is_valid_url('https://www.google.com')
        True

        >>> is_valid_url('http://thissitedoesnotexist.com')
        False
    """
    try:
        # Send a GET request to the URL and check for a successful response.
        response = requests.get(url)
        return response.status_code == 200  # Return True if status code is 200 (OK), otherwise False.
    except Exception:
        # Return False if there is an exception (invalid URL, connection error, etc.).
        return False
