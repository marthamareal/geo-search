from rest_framework import status
from rest_framework.test import APIClient

from api.tests.base import BaseTest


class TestUserRegistration(BaseTest):

    def setUp(self):
        self.client = APIClient()
        self.register_data = {
            'email': 'test@example.com',
            'password': 'pass12345'
        }

    def test_user_registration_succeeds(self):
        response = self.client.post(
            '/api/users/signup/',
            data=self.register_data,
            format='json'
        )
        self.assertEqual(
            response.json()['message'],
            'Your account has been created successfully'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_registration_missing_email_fails(self):
        self.register_data.pop('email')
        response = self.client.post(
            '/api/users/signup/',
            data=self.register_data,
            format='json'
        )
        self.assertEqual(
            response.json(), {'email': ['This field is required.']}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_registration_short_password_fails(self):
        self.register_data['password'] = 'pass'
        response = self.client.post(
            '/api/users/signup/',
            data=self.register_data,
            format='json'
        )
        self.assertEqual(
            response.json(), {
                'error': ['Password should have a minimum length of 8']
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_registration_weak_password_fails(self):
        self.register_data['password'] = 'mypassword'
        response = self.client.post(
            '/api/users/signup/',
            data=self.register_data,
            format='json'
        )
        self.assertEqual(
            response.json(), {
                'error': [
                    'Weak password. Password should at '
                    'least contain a letter and a digit.'
                ]
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
