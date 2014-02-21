"""
Contains all the methods for interacting with FireBase, a hosted JSON
database.

Public Methods:
    date_to_epoch() - datetime object to UNIX epoch timestamp
    epoch_to_date() - UNIX epoch timestamp to datetime object
    get_weather() - Returns weather information for given coordinates
    put_weather() - Stores weather information for given coordinates
"""
import json
from datetime import datetime
from django.conf import settings
import requests


def _create_weather_key(lat, lng):
    """
    Creates a properly formatted key for storing in a JSON database.

    Args:
    lat (string or float) -- latitude component of coordinate
    lng (string or float) -- longitude component of coordinate

    Returns:
    string -- key value
    """
    tmp = "%s,%s" % (lat, lng)
    return tmp.replace(".", "")


def date_to_epoch(dt):
    """ datetime object to UNIX epoch timestamp in a string """
    return str((dt - datetime(1970, 1, 1)).total_seconds())


def epoch_to_date(s):
    """ UNIX epoch timestamp in string or float to datetime object """
    return datetime.utcfromtimestamp(float(s))


def get_weather(lat, lng):
    """
    Returns weather information for given coordinates

    Args:
    lat (string or float) -- latitude component of coordinate
    lng (string or float) -- longitude component of coordinate

    Returns:
    None or Dict
    """
    url = "%s/weather/%s.json" % (settings.FIREBASE_URL,
                                  _create_weather_key(lat, lng))

    r = requests.get(url)
    if r.status_code != 200:
        return None

    return r.json()


def put_weather(lat, lng, data):
    """
    Stores weather information for given coordinates

    Args:
    lat (string or float) -- latitude component of coordinate
    lng (string or float) -- longitude component of coordinate
    data (Dict) -- weather information

    Returns:
    Bool -- True if the PUT was successful
    """
    url = "%s/weather/%s.json" % (settings.FIREBASE_URL,
                                  _create_weather_key(lat, lng))
    payload = json.dumps(data)

    r = requests.put(url, data=payload)

    return r.status_code == 200