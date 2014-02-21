from django.test import TestCase
from ForecastIO.models import ForecastIO


class ForecastIOTests(TestCase):

    def __init__(self, *args, **kwargs):
        self.json_test_data = {
            "key1": "value1",
            "key2": "value2",
            "key3": "value3",
            "list": [
                {
                    "subkey1": "subvalue1",
                    "subkey2": "subvalue2",
                    "subkey3": "subvalue3"
                },
                {
                    "subkey1": "subvalue1",
                    "subkey2": "subvalue2",
                    "subkey3": "subvalue3"
                },
                {
                    "subkey1": "subvalue1",
                    "subkey2": "subvalue2",
                    "subkey3": "subvalue3"
                }
            ]
        }

        TestCase.__init__(self, *args, **kwargs)

    def get(self, needles):
        return ForecastIO._get_value(
            self.json_test_data,
            needles
        )

    def test_json_top_level(self):
        self.assertEqual(self.get(["key1"]), self.json_test_data["key1"])
        self.assertEqual(self.get(["key2"]), self.json_test_data["key2"])
        self.assertEqual(self.get(["key3"]), self.json_test_data["key3"])
        self.assertEqual(self.get(["list"]), self.json_test_data["list"])
        self.assertEqual(self.get(["blah"]), None)

    def test_json_indexing(self):
        self.assertEqual(self.get(["list", 0]), self.json_test_data["list"][0])
        self.assertEqual(self.get(["list", 1]), self.json_test_data["list"][1])
        self.assertEqual(self.get(["list", 2]), self.json_test_data["list"][2])
        self.assertEqual(self.get(["list", 99]), None)

    def test_json_deep(self):
        self.assertEqual(
            self.get(["list", 0, "subkey1"]),
            self.json_test_data["list"][0]["subkey1"]
        )
        self.assertEqual(
            self.get(["list", 0, "subkey2"]),
            self.json_test_data["list"][0]["subkey2"]
        )
        self.assertEqual(
            self.get(["list", 0, "subkey3"]),
            self.json_test_data["list"][0]["subkey3"]
        )
        self.assertEqual(
            self.get(["list", 0, "blah"]),
            None
        )

    def test_json_optional_param(self):

        self.assertEqual(
            ForecastIO._get_value(self.json_test_data, ["list", 0, "blah"]),
            None
        )

        self.assertEqual(
            ForecastIO._get_value(self.json_test_data, ["list", 0, "blah"], 7),
            7
        )

        self.assertEqual(
            ForecastIO._get_value(
                self.json_test_data,
                ["list", 0, "blah"], "hi"
            ),
            "hi"
        )

    def test_api(self):

        # Danbury, CT
        data = ForecastIO.get_weather(41.4022, -73.4711)
        self.assertEqual(data["tz_offset"], -5)
        self.assertTrue(data["icon"])
        self.assertTrue(data["current"])
        self.assertTrue(data["high"])
        self.assertTrue(data["low"])

        # Los Angeles, CA
        data = ForecastIO.get_weather(34.05, -118.25)
        self.assertEqual(data["tz_offset"], -8)
        self.assertTrue(data["icon"])
        self.assertTrue(data["current"])
        self.assertTrue(data["high"])
        self.assertTrue(data["low"])
