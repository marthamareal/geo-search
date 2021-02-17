import requests

from django.test import TestCase
from mock import Mock
from rest_framework.exceptions import ValidationError

from api.location.validators import validate_float, validated_request_params


class TestValidators(TestCase):

    def test_validate_float_succeeds(self):
        result = validate_float('x', 3.0)
        self.assertIsInstance(result, float)

    def test_validate_float_fails(self):
        with self.assertRaises(ValidationError):
            validate_float('x', 'a')

    def test_validated_request_params_no_params(self):
        mock_request = Mock(spec=requests.Request, GET=Mock(keys=Mock()))
        mock_request.GET.keys.return_value = []
        with self.assertRaises(ValidationError):
            validated_request_params(mock_request)

    def test_validated_request_params_missing_params(self):
        mock_request = Mock(spec=requests.Request, GET=Mock(keys=Mock()))
        mock_request.GET.keys.return_value = ['x', 'y', 'n']
        with self.assertRaises(ValidationError):
            validated_request_params(mock_request)
