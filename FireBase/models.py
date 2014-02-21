import json
from datetime import datetime
from django.conf import settings
import requests


class FireBase(object):

    @staticmethod
    def _create_key(lat, lng):
        tmp = "%s,%s" % (lat, lng)
        return tmp.replace(".", "")

    @staticmethod
    def date_to_epoch(dt):
        return str((dt - datetime(1970,1,1)).total_seconds())

    @staticmethod
    def epoch_to_date(s):
        return datetime.utcfromtimestamp(float(s))


    @staticmethod
    def get_weather(lat, lng):
        url = "%s/weather/%s.json" % (settings.FIREBASE_URL,
                                      FireBase._create_key(lat, lng))

        r = requests.get(url)
        if r.status_code != 200:
            return None

        return r.json()

    @staticmethod
    def put_weather(lat, lng, data):
        url = "%s/weather/%s.json" % (settings.FIREBASE_URL,
                                      FireBase._create_key(lat, lng))
        payload = json.dumps(data)

        r = requests.put(url, data=payload)

        return r.status_code == 200
