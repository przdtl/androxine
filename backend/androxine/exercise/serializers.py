from rest_framework import serializers


class ExerciseSerializer(serializers.ModelSerializer):
    pass
    # category

    # class Meta:
    #     model = Exercise
    #     fields = ['slug',]


class ExerciseCategorySerializer(serializers.ModelSerializer):
    pass
