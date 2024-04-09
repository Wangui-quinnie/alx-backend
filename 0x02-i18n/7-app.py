from flask import request
from babel import dates
import pytz

def get_timezone():
    """
    Get the timezone for the current request.

    The timezone is determined in the following order:
    1. Check for timezone parameter in URL parameters.
    2. Find the timezone from user settings if available.
    3. Default to UTC if no timezone is provided.

    Returns:
        str: The timezone identifier.
    """
    # Check for timezone parameter in URL parameters
    timezone = request.args.get('timezone')

    # Find timezone from user settings
    if not timezone and hasattr(request, 'user') and request.user:
        timezone = request.user.get('timezone')

    # Default to UTC if no timezone is provided
    if not timezone:
        timezone = 'UTC'

    # Validate the timezone
    try:
        pytz.timezone(timezone)
    except pytz.exceptions.UnknownTimeZoneError:
        timezone = 'UTC'  # Default to UTC if the provided timezone is invalid

    return timezone
