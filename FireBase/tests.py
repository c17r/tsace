from datetime import datetime, timedelta
from django.test import TestCase
import firebase


class FireBaseTests(TestCase):

    def test_weather(self):

        expiration = datetime.utcnow() + timedelta(minutes=15)
        test = {
            "name": "test_name",
            "tz_offset": -1,
            "temp": {
                "current": -99,
                "high": -98,
                "low": -97
            },
            "comments": [],
            "expires": firebase.date_to_epoch(expiration),
            "watchers": -96
        }

        result = firebase.put_weather(-99.63, -99.31, test)
        self.assertTrue(result)

        data = firebase.get_weather(-99, -99)
        self.assertEqual(data["name"], test["name"])
        self.assertEqual(data["tz_offset"], test["tz_offset"])
        self.assertEqual(data["expires"], test["expires"])
        self.assertEqual(data["watchers"], test["watchers"])
        self.assertEqual(data["temp"]["current"], test["temp"]["current"])
        self.assertEqual(data["temp"]["high"], test["temp"]["high"])
        self.assertEqual(data["temp"]["low"], test["temp"]["low"])
