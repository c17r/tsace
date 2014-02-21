from datetime import datetime, timedelta
from FireBase import FireBase
from ForecastIO import ForecastIO

class Weather(object):

    @staticmethod
    def get_weather(lat, lng, name):

        data = FireBase.get_weather(lat, lng)
        if data:
            utc = datetime.utcnow()
            if FireBase.epoch_to_date(data["expires"]) > utc:
                return data
        data = data or {}

        current = ForecastIO.get_weather(lat, lng)
        new = {
            "name": name,
            "tz_offset": current["tz_offset"],
            "temp": {
                "current": current["current"],
                "high": current["high"],
                "low": current["low"],
                "icon": current["icon"],
            },
            "comments": [],
            "expires": FireBase.date_to_epoch((datetime.utcnow() +
                                               timedelta(minutes=15))),
            "watchers": data.get("watchers", 0)
        }
        result = FireBase.put_weather(lat, lng, new)

        return new
