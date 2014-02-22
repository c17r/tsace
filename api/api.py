# coding=utf-8
"""
Main Weather API functionality, used by both front-end generation and API calls

Public Methods:
    get_weather -- Returns weather information for a given coordinate
    get_saved_cities -- Returns weather information for all cities that a user
        has saved to their profile
    remove_city_from_user -- Removes specified city from user's profile
    add_city_to_user -- Adds new city to user's profile
"""
import uuid
from datetime import datetime, timedelta
import FireBase
import ForecastIO


class MissingUserError(Exception):
    """
    Thrown if an action has been requested for a user that doesn't exist in
        the database.
    """
    pass


def _f_to_c(f):
    """
    Converts temperature in Fahrenheit to Celsius

    Args:
    f (real) -- Fahrenheit

    Returns:
    real -- Celsius
    """
    return (f-32)*5.0/9.0


def _create_weather_key(lat, lng):
    """
    Creates a database legal key for the given coordinate.

    Args:
    lat (string or float) -- latitude of the coordinate
    lng (string or float) -- longitude of the coordinate

    Returns:
    string -- proper key for database
    """
    tmp = "%s,%s" % (lat, lng)
    return tmp.replace(".", "")


def get_weather(lat, lng, name):
    """
    Gets weather information for a given coordinate.  Information may be up to
        15 minutes old.

    Args:
    lat (string or float) -- latitude of the coordinate
    lng (string or float) -- longitude of the coordinate
    name (string) -- Human readable name of the coordinate

    Returns
    Dict of weather information (see fresh_weather())
    """
    data = FireBase.get_weather(lat, lng)
    if check_weather(data):
        return data

    weather = fresh_weather(lat, lng, name, data)
    FireBase.put_weather(lat, lng, weather)

    return weather


def check_weather(weather):
    """
    Checks to see if the Weather information is too stale and should be
        refreshed.

    Args:
    weather (Dict) -- object returned from get_weather()

    Returns:
    Bool -- True if the weather information is still fresh
    """
    if not weather:
        return False

    utc = datetime.utcnow()
    expires = FireBase.epoch_to_date(weather["expires"])

    return expires > utc


def fresh_weather(lat, lng, name, stale=None):
    """
    Makes a call to the weather api-endpoint to get fresh weather information

    Args:
    lat (string or float) -- latitude of the coordinate
    lng (string or float) -- longitude of the coordinate
    name (string) -- Human readable name of the coordinate
    stale (Dict) -- the now-stale weather information retrieved from
        get_weather()

    Returns
    Dict {
        "coords" (Dict) {
            "latitude" (string or float) -- latitude of the coordinate
            "longitude" (string or float) -- longitude of the coordinate
        }
        "expires" (float) -- UNX timestamp for when the temperature data
            should be discarded.
        "key" (string) -- Database key for the coordinate
        "name" (string) -- Human readable name of the coordinate
        "temp" (Dict) {
            "current" (string) -- current temperature for the coordinate
            "high" (string) -- daily high temperature for the coordinate
            "icon" (string) -- machine readable summary of daily weather.
                (i.e. rain, snow, partly-cloudy-day, clear-night, etc).
            "low" (string) -- daily low temperature for the coordinate
            "summary" (string) -- human readable description of forecast
        }
        "tz_offset" (string) -- Timezone for the coordinate
        "watchers" (number) -- how many users have saved this coordinate
    }
    """
    watchers = 0
    if stale:
        watchers = stale.get("watchers", 0)

    current = ForecastIO.get_weather(lat, lng)

    current_f = round(current["current"])
    current_c = round(_f_to_c(current_f))
    current_s = "%d°F/%d°C" % (current_f, current_c)

    high_f = round(current["high"])
    high_c = round(_f_to_c(high_f))
    high_s = "%d°F/%d°C" % (high_f, high_c)

    low_f = round(current["low"])
    low_c = round(_f_to_c(low_f))
    low_s = "%d°F/%d°C" % (low_f, low_c)

    weather = {
        "name": name,
        "key": _create_weather_key(lat, lng),
        "coords": {
            "latitude": lat,
            "longitude": lng
        },
        "tz_offset": current["tz_offset"],
        "temp": {
            "current": current_s,
            "high": high_s,
            "low": low_s,
            "icon": current["icon"],
            "summary": current["summary"],
        },
        "comments": [],
        "expires": FireBase.date_to_epoch((datetime.utcnow() +
                                           timedelta(minutes=15))),
        "watchers": watchers
    }
    return weather


def get_saved_cities(uid):
    """
    Gets the weather information for all the locations listed in the Places
        List of the user's database record.

    Args:
    uid (string) -- the user's key

    Returns:
    None if the user doesn't exist in the database.
    List of weather information (see get_weather())
    """
    user_data = FireBase.get_user(uid)
    if not user_data:
        return None

    city_data = []
    for place in user_data["places"]:
        weather = FireBase.get_weather_by_key(place)

        if not check_weather(weather):
            lat = weather["coords"]["latitude"]
            lng = weather["coords"]["longitude"]
            name = weather["name"]
            weather = fresh_weather(lat, lng, name, weather)
            FireBase.put_weather(lat, lng, weather)

        city_data.append(weather)

    return city_data


def create_new_user():
    """
    Creates a new user in database and returns information.

    Returns:
    uid (string) -- user's key
    data (Dict) {
        "temp_method" (string) -- "F" or "C" for which temperature scale.
        "Places" (List of String) -- keys for places the users wish to save
    }
    """
    uid = uuid.uuid4()
    data = {
        "temp_method": "F",
        "places": []
    }
    FireBase.put_user(uid, data)
    return uid, data


def remove_city_from_user(uid, city_key):
    """
    Removes the passed in city from the user's database record.

    Args:
    uid (string) -- The user's key
    city_key (string) -- the location to remove from the places List in the
        user's record

    Returns:
    Bool -- True if the removal was saved to the database

    Returns:
    Bool -- True if the users is saved back to the database

    Raises:
    MissingUserError -- if the uid doesn't exist
    """
    def remove_city(user):
        if city_key in user["places"]:
            user["places"].remove(city_key)
        return user

    return _func_to_user(uid, remove_city)


def add_city_to_user(uid, city_key):
    """
    Adds the passed in city to the user's database record.

    Args:
    uid (string) -- The user's key
    city_key (string) -- the location to add to the places List in the user's
        record

    Returns:
    Bool -- True if the users is saved back to the database

    Raises:
    MissingUserError -- if the uid doesn't exist
    """
    def add_city(user):
        if city_key not in user["places"]:
            user["places"].append(city_key)
        return user

    return _func_to_user(uid, add_city)


def _func_to_user(uid, func):
    """
    Internal function for doing actions against a user.  Gets the user from
        the database, calls the provided function, and then updates the user
        back in the database.

    Args:
    uid (string) -- The user's key
    func (function) -- activity to perform on the user record

    Returns:
    Bool -- True if the users is saved back to the database

    Raises:
    MissingUserError -- if the uid doesn't exist
    """
    user = FireBase.get_user(uid)
    if not user:
        raise MissingUserError

    user = func(user)

    return FireBase.put_user(uid, user)
