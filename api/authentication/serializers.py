import re

from django.contrib.auth import authenticate
from rest_framework import serializers

from api.authentication.models import GeoUser


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        write_only=True
    )

    class Meta:
        model = GeoUser
        fields = '__all__'
        read_only_fields = 'password',

    def validate(self, attrs):
        password = attrs.get('password')
        if len(password) < 8:
            raise serializers.ValidationError(
                'Password should have a minimum length of 8'
            )
        if password.isdigit() or not re.search('[0-9]', password):
            raise serializers.ValidationError(
                'Weak password. Password should at least contain a letter and a digit.'
            )

        return attrs

    def create(self, validated_data):
        return GeoUser.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    id = serializers.UUIDField(read_only=True)
    email = serializers.EmailField()
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        # Raise an exception if an email is not provided.
        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        # Raise an exception if a password is not provided.
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        # The `authenticate` method is provided by Django and handles checking
        # for a user that matches this email/password combination. Hence
        # we pass `email` as the `username` value because, in our User
        # model, we set `USERNAME_FIELD` as `email`.
        user = authenticate(username=email, password=password)

        # If no user was found matching this email/password combination then
        # `authenticate` will return `None`. Raise an exception in this case.
        if user is None:
            raise serializers.ValidationError(
                'Unable to login with the provided credentials.'
            )
        return {
            'id': user.id,
            'email': user.email,
            'token': user.token
        }

