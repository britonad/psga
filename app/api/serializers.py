from rest_framework import serializers


# Bare serializers are faster than ModelSerializers.
# See: https://hakibenita.com/django-rest-framework-slow
class ShipSerializer(serializers.Serializer):
    imo = serializers.IntegerField()
    name = serializers.CharField(max_length=17)


class ShipPositionsSerializer(serializers.Serializer):
    latitude = serializers.CharField(max_length=20)
    longitude = serializers.CharField(max_length=19)
    timestamp = serializers.DateTimeField(required=False)
