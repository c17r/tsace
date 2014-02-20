from datetime import datetime, timedelta
from django.conf import settings
import requests


class ForecastIO(object):

    @staticmethod
    def _get_value(haystack, needles, missing_value=None):
        try:
            ptr = haystack
            for needle in needles[:-1]:
                ptr = ptr[needle]
            return ptr[needles[-1]]
        except (KeyError, IndexError):
            return missing_value

    @staticmethod
    def get_weather(lat, lng):
        url = "https://api.forecast.io/forecast/%s/%s,%s" % (
            settings.FORECAST_IO_KEY,
            lat,
            lng
        )

        r = requests.get(url, params={
            "units": "us",
            "exclude": "minutely,hourly,alerts,flags"
        })
        data = r.json()

        return {
            "tz_offset": ForecastIO._get_value(data, ["offset"]),
            "icon": ForecastIO._get_value(data, ["currently", "icon"]),
            "current": ForecastIO._get_value(data,
                                             ["currently", "temperature"]),
            "high": ForecastIO._get_value(data,
                                          ["daily", "data", 0, "temperatureMax"]),
            "low": ForecastIO._get_value(data,
                                         ["daily", "data", 0, "temperatureMin"])
        }
