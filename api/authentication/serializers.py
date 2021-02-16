import re

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

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


class LoginSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['id'] = str(self.user.id)
        data['email'] = str(self.user.email)
        data['access'] = str(refresh.access_token)
        data['refresh'] = str(refresh)

        return data
