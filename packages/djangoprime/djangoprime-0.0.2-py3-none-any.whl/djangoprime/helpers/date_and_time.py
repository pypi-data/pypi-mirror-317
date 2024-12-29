from datetime import datetime, timezone

from django.contrib.humanize.templatetags.humanize import naturaltime, naturalday
from django.utils import timezone as django_timezone


def make_and_get_datetime_aware(date_string):
    """
    Takes a date string in a specific format and returns an aware datetime object.

    The function first converts a naive datetime object (lacking timezone information) into an aware
    datetime object by attaching the current timezone information.

    Args:
        date_string (str): The date string in the format '%Y-%m-%d %H:%M:%S.%f', representing a datetime.

    Returns:
        datetime: An aware datetime object with the timezone information attached, or None if an error occurs.
    """
    try:
        # Parse the date string into a naive datetime object (without timezone information)
        naive_datetime = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S.%f')

        # Make the datetime object aware by attaching the current timezone
        aware_datetime = django_timezone.make_aware(naive_datetime, django_timezone.get_current_timezone())

        # Return the aware datetime object
        return aware_datetime
    except Exception as e:
        # Handle any exceptions that might occur during parsing or timezone conversion
        print(f"Error: {e}")
        return None


def get_current_timestamp():
    """
    Returns the current timestamp in ISO 8601 format with the current timezone.

    This function retrieves the current UTC time, then converts it to the local time zone
    before formatting it in ISO 8601 format.

    Returns:
        str: The current timestamp in ISO 8601 format with the local timezone.
    """
    # Get the current time in UTC, then convert it to the local timezone and return the ISO format string
    return datetime.now(timezone.utc).astimezone().isoformat()


def get_django_date_and_times(date_string):
    """
    Takes a date string and returns a dictionary with three representations of the date:
    - The original timestamp.
    - The "natural time" format (e.g., "3 minutes ago").
    - The "natural day" format (e.g., "Yesterday" or "Monday").

    Args:
        date_string (str): The date string representing the timestamp to be processed.

    Returns:
        dict: A dictionary with the original timestamp, naturaltime, and naturalday.
    """
    return {
        'timestamp': date_string,  # Original timestamp
        'naturaltime': naturaltime(date_string),  # Human-readable time ago (e.g., "2 hours ago")
        'naturalday': naturalday(date_string)  # Human-readable day (e.g., "Yesterday")
    }
