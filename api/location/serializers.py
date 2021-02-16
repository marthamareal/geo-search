from rest_framework import serializers

from api.location.models import RequestHistory, Location


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = '__all__'


class RequestHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = RequestHistory
        fields = '__all__'
        read_only_fields = ['user']

    def validate(self, attrs):
        request = self.context.get('request')
        attrs['user'] = request.user
        return attrs
