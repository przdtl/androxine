from rest_framework import serializers


class CalculateSerializer(serializers.Serializer):
    weight = serializers.FloatField(
        min_value=0.1,
        max_value=1000.0,
    )
    reps = serializers.IntegerField(
        min_value=2,
        max_value=15,
    )
