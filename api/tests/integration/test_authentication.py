from django.contrib.auth.hashers import make_password
from model_bakery import baker

from rest_framework import status
from rest_framework.test import APIClient

from django.test import TestCase
from django.urls import reverse


class TestUserRegistration(TestCase):

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


class TestUserLogin(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = baker.make(
            'authentication.GeoUser',
            password=make_password('pass1234')
        )

    def test_user_login_with_correct_credentials_succeeds(self):
        response = self.client.post(
            reverse('login'),
            data={
                'email': self.user.email,
                'password': 'pass1234'
            },
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_login_with_wrong_credentials_succeeds(self):
        response = self.client.post(
            reverse('login'),
            data={
                'email': self.user.email,
                'password': 'wrongpassword'
            },
            format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_login_with_missing_credentials_succeeds(self):
        response = self.client.post(
            reverse('login'),
            data={
                'email': self.user.email
            },
            format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
