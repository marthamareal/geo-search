from django.contrib.auth.hashers import make_password
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APIClient

from api.tests.base import BaseTest


class TestPointSearch(BaseTest):

    def setUp(self):
        self.user = baker.make(
            'authentication.GeoUser',
            password=make_password('pass1234')
        )
        baker.make('location.Location', _quantity=5)

    def test_get_points_with_correct_params_succeeds(self):
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        response = self.client.get(
            '/api/points/get_locations?x=2&y=3&n=5&operation_type=nearest',
            follow=True,
        )
        self.assertEqual(
            len(response.json()), 5
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_points_with_missing_params_fails(self):
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        response = self.client.get(
            '/api/points/get_locations',
            follow=True,
        )
        self.assertEqual(
            response.json()['error'],
            'All params x, y, n and operation_type are required'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_points_with_invalid_x_param_fails(self):
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        response = self.client.get(
            '/api/points/get_locations?x=a&y=3&n=5&operation_type=nearest',
            follow=True,
        )
        self.assertEqual(
            response.json()['error'],
            'x must be of type float.'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_points_with_invalid_y_param_fails(self):
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        response = self.client.get(
            '/api/points/get_locations?x=5&y=b&n=5&operation_type=nearest',
            follow=True,
        )
        self.assertEqual(
            response.json()['error'],
            'y must be of type float.'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_points_with_invalid_n_param_fails(self):
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        response = self.client.get(
            '/api/points/get_locations?x=2&y=3&n=5.9&operation_type=nearest',
            follow=True,
        )
        self.assertEqual(
            response.json()['error'],
            'n must be of type int.'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_points_with_invalid_operation_type_param_fails(self):
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        response = self.client.get(
            '/api/points/get_locations?x=2&y=3&n=5&operation_type=invalid',
            follow=True,
        )
        self.assertEqual(
            response.json()['error'],
            'operation_type must either be nearest or furthest'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
