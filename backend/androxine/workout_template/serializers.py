from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from workout_template.models import (
    WorkoutTemplate,
    ExerciseInWorkoutTemplate,
    ExerciseApproachInWorkoutTemplate,
)


class WorkoutTemplateReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutTemplate
        fields = '__all__'
        read_only_fields = ['id', 'created_by']


class WorkoutTemplateWriteSerializer(serializers.ModelSerializer):
    break_between_approaches = serializers.IntegerField(
        required=False,
        default=120,  # TODO: add dependence on global user workout settings
    )
    created_by = serializers.UUIDField(
        source='created_by_id',
        required=False,
        help_text='this field is calculated automatically based on the data of the logged-in user',
    )

    class Meta:
        model = WorkoutTemplate
        fields = '__all__'
        read_only_fields = ['id', 'created_by']
        validators = [
            UniqueTogetherValidator(
                queryset=WorkoutTemplate.objects.all(),
                fields=['created_by', 'name'],
                message=_(
                    'Workout template with this name for this user already exists'),
            )
        ]


class ExerciseInWorkoutTemplateReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseInWorkoutTemplate
        fields = '__all__'
        read_only_fields = ['id', 'template']


class ExerciseInWorkoutTemplateWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseInWorkoutTemplate
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=ExerciseInWorkoutTemplate.objects.all(),
                fields=['template', 'exercise'],
                message=_(
                    'Exercise in this template for this user already exists'),
            )
        ]


class ExerciseApproachInWorkoutTemplateReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseApproachInWorkoutTemplate
        fields = '__all__'
        read_only_fields = ['id', 'exercise_in_workout_template']


class ExerciseApproachInWorkoutTemplateWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseApproachInWorkoutTemplate
        fields = '__all__'
        read_only_fields = ['id']
