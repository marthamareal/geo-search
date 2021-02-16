"""Base test class for project."""

from django.test import TestCase
from django.urls import reverse


class BaseTest(TestCase):

    def login_user(self, client, user):
        login_response = client.post(
            reverse('login'),
            data={
                'email': user.email,
                'password': 'pass1234'
            },
            format='json').json()
        client.credentials(
            HTTP_AUTHORIZATION='bearer ' + login_response['access']
        )
