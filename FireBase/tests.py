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

        result = firebase.put_weather("test-fb-lat", "test-fb-lng", test)
        self.assertTrue(result)

        data = firebase.get_weather("test-fb-lat", "test-fb-lng")
        self.assertTrue(data)
        self.assertEqual(data["name"], test["name"])
        self.assertEqual(data["tz_offset"], test["tz_offset"])
        self.assertEqual(data["expires"], test["expires"])
        self.assertEqual(data["watchers"], test["watchers"])
        self.assertEqual(data["temp"]["current"], test["temp"]["current"])
        self.assertEqual(data["temp"]["high"], test["temp"]["high"])
        self.assertEqual(data["temp"]["low"], test["temp"]["low"])

    def test_user_1(self):

        uid = "test-fb-user"
        test = {
            "temp_method": "F",
            "places": [
                "string1",
                "string2",
                "string3"
            ]
        }

        result = firebase.put_user(uid, test)
        self.assertTrue(result)

        data = firebase.get_user(uid)
        self.assertTrue(data)
        self.assertEqual(data["temp_method"], test["temp_method"])
        self.assertEqual(data["places"][0], test["places"][0])
        self.assertEqual(data["places"][1], test["places"][1])
        self.assertEqual(data["places"][2], test["places"][2])

    def test_user_2(self):

        uid = "test-fb-user"
        test = {
            "temp_method": "F",
            "places": []
        }

        result = firebase.put_user(uid, test)
        self.assertTrue(result)

        data = firebase.get_user(uid)
        self.assertTrue(data)
        self.assertEqual(data["temp_method"], test["temp_method"])
        self.assertEqual(data["places"], test["places"])
