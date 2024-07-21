from rest_framework import serializers

from exercise.models import Exercise


class ExerciseSerializer(serializers.ModelSerializer):
    category = serializers.CharField(
        required=False,
    )
    name = serializers.CharField(
        required=False,
    )

    class Meta:
        model = Exercise
        fields = '__all__'


class ExerciseCategorySerializer(serializers.ModelSerializer):
    pass
