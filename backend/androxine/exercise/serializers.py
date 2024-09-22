from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from exercise.models import Exercise, ExerciseCategory, UserExerciseSettings


class ExerciseListSerializer(serializers.ModelSerializer):
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


class ExerciseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = '__all__'
        read_only_fields = ['id', 'slug']


class ExerciseListSwaggerSerializer(serializers.ModelSerializer):
    category = serializers.CharField(
        source='category__name',
        required=False,
    )
    name = serializers.CharField(
        required=False,
    )
    ordering = serializers.CharField(
        required=False,
        default='name',
    )

    def validate(self, attrs):
        available_ordering_values = ['name', '-name']
        ordering = attrs['ordering']
        if ordering:
            if ordering not in available_ordering_values:
                raise serializers.ValidationError('Invalid ordering value')

        return attrs

    class Meta:
        model = Exercise
        fields = '__all__'
        read_only_fields = ['id', 'slug']


class ExericseManageSerializer(serializers.ModelSerializer):
    exercise_slug = serializers.CharField(
        source='exercise.slug',
        read_only=True,
    )

    class Meta:
        model = Exercise
        fields = '__all__'


class ExerciseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseCategory
        fields = '__all__'


class UserExerciseSettingsManageSerializer(serializers.ModelSerializer):
    exercise_slug = serializers.CharField(
        source='exercise.slug',
        read_only=True,
    )

    class Meta:
        model = UserExerciseSettings
        fields = '__all__'
        read_only_fields = ['id', 'user', 'exercise_slug', 'exercise']


class UserExerciseSettingsManageSwaggerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserExerciseSettings
        fields = ['one_time_maximum']


class UserExerciseSettingsListSwaggerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserExerciseSettings
        fields = ['exercise', 'one_time_maximum']


class UserExerciseSettingsListCreateSerializer(serializers.ModelSerializer):
    exercise_slug = serializers.CharField(
        source='exercise.slug',
        read_only=True,
    )

    class Meta:
        model = UserExerciseSettings
        fields = '__all__'
        read_only_fields = ['exercise_slug']
        validators = [
            UniqueTogetherValidator(
                queryset=UserExerciseSettings.objects.all(),
                fields=['user', 'exercise'],
                message=_(
                    'An instance of the settings for this user already exists'),
            )
        ]
