import jwt
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, get_authorization_header

from api.authentication.models import GeoUser
from api.geosearch.settings import SECRET_KEY


class JWTAuthentication(BaseAuthentication):

    def authenticate(self, request, **kwargs):

        token = JWTAuthentication.get_token(request, kwargs)

        if not token:
            return None

        try:
            decoded = jwt.decode(token, SECRET_KEY)

            user_id = decoded['id']
            email = decoded['email']

            user = GeoUser.objects.get(id=user_id, email=email)

            return user, token

        except jwt.InvalidTokenError or jwt.DecodeError:
            raise exceptions.AuthenticationFailed("Invalid token ")

        except jwt.ExpiredSignature:
            raise exceptions.AuthenticationFailed("Token expired Login again to get new token")

    @staticmethod
    def get_token(request, kwargs):

        if "token" in kwargs:
            token = kwargs["token"]
        else:
            token = get_authorization_header(request)

        return token
