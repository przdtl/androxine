from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from exercise.models import Exercise, ExerciseCategory, UserExerciseSettings


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
        read_only_fields = ['slug']


class ExerciseListSwaggerSerializer(serializers.ModelSerializer):
    category = serializers.CharField(
        source='category__name',
        required=False,
    )
    name = serializers.CharField(
        required=False,
    )

    class Meta:
        model = Exercise
        fields = ['category', 'name']


class ExerciseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseCategory
        fields = '__all__'


class ReadUserExerciseSettingsSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(
        source='exercise.slug',
        read_only=True,
    )

    class Meta:
        model = UserExerciseSettings
        fields = ['user', 'slug', 'one_time_maximum']
        read_only_fields = ['user']


class WriteUserExerciseSettingsSerializer(serializers.ModelSerializer):
    exercise = serializers.SlugRelatedField(
        queryset=Exercise.objects.all(),
        slug_field='slug',
    )
    user = serializers.UUIDField(
        source='user_id',
        required=False,
        help_text='this field is calculated automatically based on the data of the logged-in user',
    )

    class Meta:
        model = UserExerciseSettings
        fields = ['user', 'exercise', 'one_time_maximum']
        validators = [
            UniqueTogetherValidator(
                queryset=UserExerciseSettings.objects.all(),
                fields=['user', 'exercise'],
                message=_(
                    'An instance of the settings for this user already exists'),
            )
        ]
