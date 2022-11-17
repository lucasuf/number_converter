from django.conf import settings
from django.test import SimpleTestCase, override_settings
from django.urls import reverse
from rest_framework import status

from converter_app.serializers import MAX_INTEGER_VALUE

HOST = "http://localhost:8000"
throttling_test_settings = settings.REST_FRAMEWORK.copy()
throttling_test_settings["DEFAULT_THROTTLE_RATES"]["anon"] = None


@override_settings(REST_FRAMEWORK=throttling_test_settings)
class NumberToEnglishConverterEndpointTestCase(SimpleTestCase):
    def setUp(self):
        self.url = HOST + reverse("rest_number_to_english_converter")

    def test_get_with_valid_query_param(self):
        numbers = {
            "12345678": "twelve million three hundred forty five thousand six hundred seventy eight",
            "12": "twelve",
            "10000000": "ten million",
            "12319": "twelve thousand three hundred nineteen",
            "90013": "ninety thousand thirteen",
            "000": "zero",
            "999999999999": "nine hundred ninety nine billion nine hundred ninety nine million nine "
                            "hundred ninety nine thousand nine hundred ninety nine",
        }
        for key, value in numbers.items():
            response = self.client.get(self.url, {"number": key})
            expected = {
                "status": "ok",
                "number_in_english": value,
            }

            data = response.json()

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(data, expected)

    def test_get_with_valid_query_param_negative_number(self):
        response = self.client.get(self.url, {"number": "-1234"})
        expected = {
            "status": "ok",
            "number_in_english": "negative one thousand two hundred thirty four",
        }

        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, expected)

    def test_get_with_invalid_query_param_text(self):
        response = self.client.get(self.url, {"number": "invalid-str"})
        expected = {
            "status": "error",
            "errors": {"number": ["A valid integer is required."]},
        }

        data = response.json()
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            "valid integer is required",
        )
        self.assertEqual(data, expected)

    def test_get_with_invalid_query_param_over_max_integer_value(self):
        response = self.client.get(self.url, {"number": MAX_INTEGER_VALUE + 1})
        expected = {
            "status": "error",
            "errors": {
                "number": [
                    f"Ensure this value is less than or equal to {str(MAX_INTEGER_VALUE)}."
                ]
            },
        }

        data = response.json()
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            "valid integer is required",
        )
        self.assertEqual(data, expected)

    def test_get_without_query_param(self):
        response = self.client.get(self.url)
        expected = {
            "status": "error",
            "errors": {"number": ["This field is required."]},
        }

        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, "query param is required"
        )
        self.assertEqual(data, expected)

    def test_post_with_valid_data(self):
        response = self.client.post(self.url, data={"number": "12345678"})
        expected = {
            "status": "ok",
            "number_in_english": "twelve million three hundred forty five thousand six hundred seventy eight",
        }

        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, expected)

    def test_get_reached_throttle_limit(self):
        new_throttling_test_settings = throttling_test_settings.copy()
        new_throttling_test_settings["DEFAULT_THROTTLE_RATES"]["anon"] = "4/min"
        override_settings(REST_FRAMEWORK=new_throttling_test_settings)

        for _ in range(4):
            response = self.client.get(self.url, {"number": "12345678"})
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(self.url, {"number": "12345678"})
        self.assertEqual(
            response.status_code,
            status.HTTP_429_TOO_MANY_REQUESTS,
            "reached throttle limit",
        )

        return_settings = throttling_test_settings.copy()
        return_settings["DEFAULT_THROTTLE_RATES"]["anon"] = None
        override_settings(REST_FRAMEWORK=return_settings)
