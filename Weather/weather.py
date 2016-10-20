"""
Contains all the methods for interactive with Dark Sky's weather API
service.

Public Methods:
    get_weather -- Returns weather information for a given coordinate
"""
from django.conf import settings
import requests


def _get_value(haystack, needles, missing_value=None):
    """
    Safely traverses a many-level dictionary and returns the key value.

    Args:
    haystack (Dict) -- the thing we want to traverse
    needles (List of str or num) -- the traversal path through the
        haystack.  The last item on the list is the key used for returning
        a value.
    missing_value -- If any stop on the traversal path or the key itself
        is not found, return this value to the user (default None).

    Returns:

    """
    try:
        ptr = haystack
        for needle in needles[:-1]:
            ptr = ptr[needle]
        return ptr[needles[-1]]
    except (KeyError, IndexError):
        return missing_value


def get_weather(lat, lng):
    """
    Returns weather information for a given coordinate

    Args:
    lat (string or float) -- latitude component of coordinate
    lng (string or float) -- longitude component of coordinate

    Returns:
    Dict {
        "tz_offset" (string) -- Timezone for the coordinates
        "icon" (string) -- represents current weather conditions
            (e.g. clear-day, partly-cloudy-night, etc)
        "current" (real) -- current temperature in F
        "high" (real) -- high temperature for the day in F
        "low" (real) -- low temperature for the day in F
        "summary" (string) -- human readable forecast description
    }
    """
    url = "https://api.darksky.net/forecast/%s/%s,%s" % (
        settings.WEATHER_API_KEY,
        lat,
        lng
    )

    r = requests.get(url, params={
        "units": "us",
        "exclude": "minutely,hourly,alerts,flags"
    })
    data = r.json()

    return {
        "tz_offset": _get_value(data, ["timezone"]),
        "icon": _get_value(data, ["currently", "icon"]),
        "current": _get_value(data, ["currently", "temperature"]),
        "high": _get_value(data, ["daily", "data", 0, "temperatureMax"]),
        "low": _get_value(data, ["daily", "data", 0, "temperatureMin"]),
        "summary": _get_value(data, ["currently", "summary"])
    }
