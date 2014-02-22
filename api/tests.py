from datetime import datetime, timedelta
from django.test import TestCase
import api
import FireBase


class APITest(TestCase):

    def test_get_weather_cache(self):
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
            "expires": FireBase.date_to_epoch(expiration),
            "watchers": -96
        }

        result = FireBase.put_weather("test-api-lat", "test-api-lng", test)
        self.assertTrue(result)

        data = api.get_weather("test-api-lat", "test-api-lng", test["name"])
        self.assertEqual(data["name"], test["name"])
        self.assertEqual(data["tz_offset"], test["tz_offset"])
        self.assertEqual(data["expires"], test["expires"])
        self.assertEqual(data["watchers"], test["watchers"])
        self.assertEqual(data["temp"]["current"], test["temp"]["current"])
        self.assertEqual(data["temp"]["high"], test["temp"]["high"])
        self.assertEqual(data["temp"]["low"], test["temp"]["low"])

    def test_check_weather_good(self):
        utc = datetime.utcnow()
        expires = utc + timedelta(weeks=1)
        weather = {"expires": FireBase.date_to_epoch(expires)}

        self.assertTrue(api.check_weather(weather))

    def test_check_weather_bad(self):
        utc = datetime.utcnow()
        expires = utc - timedelta(weeks=1)
        weather = {"expires": FireBase.date_to_epoch(expires)}

        self.assertFalse(api.check_weather(weather))

    def test_create_new(self):
        test = {
            "temp_method": "F",
            "places": []
        }
        uid, data = api.create_new_user()

        self.assertEqual(data["temp_method"], test["temp_method"])
        self.assertEqual(data["places"], test["places"])

        data = FireBase.get_user(uid)
        self.assertEqual(data["temp_method"], test["temp_method"])
        self.assertEqual(len(data["places"]), len(test["places"]))

    def test_get_saved_cities_no_user(self):
        uid = "test-api-non-user"
        data = api.get_saved_cities(uid)

        self.assertTrue(len(data) == 0)

    def test_get_saved_cities_no_cities(self):
        test = {
            "temp_method": "F",
            "places": []
        }
        uid = "test-api-user"
        result = FireBase.put_user(uid, test)
        self.assertTrue(result)

        data = api.get_saved_cities(uid)
        self.assertListEqual(data, [])

    def test_get_saved_cities_1(self):
        expiration = datetime.utcnow() + timedelta(minutes=15)
        test_city = {
            "name": "test_name",
            "tz_offset": -1,
            "temp": {
                "current": -99,
                "high": -98,
                "low": -97
            },
            "comments": [],
            "expires": FireBase.date_to_epoch(expiration),
            "watchers": -96
        }

        result = FireBase.put_weather("test-api-lat",
                                      "test-api-lng", test_city)
        self.assertTrue(result)

        test_user = {
            "temp_method": "F",
            "places": ["test-api-lat,test-api-lng"]
        }
        uid = "test-api-user"
        result = FireBase.put_user(uid, test_user)
        self.assertTrue(result)

        data = api.get_saved_cities(uid)
        self.assertTrue(len(data) == 1)

        data = data[0]
        self.assertEqual(data["name"], test_city["name"])
        self.assertEqual(data["tz_offset"], test_city["tz_offset"])
        self.assertEqual(data["expires"], test_city["expires"])
        self.assertEqual(data["watchers"], test_city["watchers"])
        self.assertEqual(data["temp"]["current"], test_city["temp"]["current"])
        self.assertEqual(data["temp"]["high"], test_city["temp"]["high"])
        self.assertEqual(data["temp"]["low"], test_city["temp"]["low"])

    def test_add_city(self):
        test_user = {
            "temp_method": "F",
            "places": [
                "keep-1", "keep-2", "keep-3"
            ]
        }
        uid = "test-api-user"
        result = FireBase.put_user(uid, test_user)
        self.assertTrue(result)

        result = api.add_city_to_user(uid, "add-1")
        self.assertTrue(result)

        data = FireBase.get_user(uid)

        for place in test_user["places"]:
            self.assertIn(place, data["places"])

        self.assertIn("add-1", data["places"])

    def test_remove_city(self):
        test_user = {
            "temp_method": "F",
            "places": [
                "keep-1", "keep-2", "keep-3", "remove-1", "keep-4"
            ]
        }
        uid = "test-api-user"
        result = FireBase.put_user(uid, test_user)
        self.assertTrue(result)

        result = api.remove_city_from_user(uid, "remove-1")
        self.assertTrue(result)

        data = FireBase.get_user(uid)

        for place in test_user["places"]:
            if "keep" in place:
                self.assertIn(place, data["places"])
            else:
                self.assertNotIn(place, data["places"])

    def test_f_to_c_1(self):
        f = 32
        c = api._f_to_c(f)
        self.assertEqual(c, 0)

    def test_f_to_c_2(self):
        f = 212
        c = api._f_to_c(f)
        self.assertEqual(c, 100)
