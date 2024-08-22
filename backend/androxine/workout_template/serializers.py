from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from workout_template.models import (
    WorkoutTemplate,
    ExerciseInWorkoutTemplate,
    ExerciseApproachInWorkoutTemplate,
)


class WorkoutTemplateCreateSwaggerSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutTemplate
        fields = ['break_between_approaches', 'name']


class WorkoutTemplateReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutTemplate
        fields = '__all__'
        read_only_fields = ['id', 'created_by']


class WorkoutTemplateListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutTemplate
        fields = '__all__'
        read_only_fields = ['id']
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


class TemplateIdForExerciseInWorkoutTemplateSerializer(serializers.ModelSerializer):
    template_id = serializers.UUIDField(
        source='id',
        required=True,
    )

    class Meta:
        model = WorkoutTemplate
        fields = ['template_id']


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


class ExerciseInWorkoutTemplateOrderSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(
        required=True,
    )
    ordinal_number = serializers.IntegerField(
        required=True,
    )
    exercise_slug = serializers.CharField(
        source='exercise.slug',
        read_only=True,
    )

    class Meta:
        model = ExerciseInWorkoutTemplate
        fields = '__all__'
        read_only_fields = ['template', 'exercise',
                            'ordinal_number', 'exercise_slug']


class ExerciseInWorkoutTemplateReorderSerializer(serializers.Serializer):
    exercises = ExerciseInWorkoutTemplateOrderSerializer(many=True)
    template = serializers.UUIDField()

    def validate(self, attrs):
        exercises = attrs['exercises']
        exercises_count = len(exercises)
        exercises_order_list = [False] * exercises_count

        for exercise_dict in exercises:
            ordinal_number = exercise_dict['ordinal_number']
            index = ordinal_number - 1
            if not 1 <= ordinal_number <= exercises_count or exercises_order_list[index]:
                raise ValidationError(
                    {'ordinal_number': 'Incorrect ordinal numbers were passed'})

            exercises_order_list[index] = True

        return super().validate(attrs)


class ExerciseInTemplateIdForExerciseApproachInWorkoutTemplateSerializer(serializers.ModelSerializer):
    exercise_in_template_id = serializers.UUIDField(
        source='id',
        required=True,
    )

    class Meta:
        model = ExerciseInWorkoutTemplate
        fields = ['exercise_in_template_id']


class ExerciseApproachInWorkoutTemplateReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseApproachInWorkoutTemplate
        fields = '__all__'
        read_only_fields = ['id', 'exercise_in_workout_template']


class ExerciseApproachInWorkoutTemplateWriteSerializer(serializers.ModelSerializer):
    relative_weight = serializers.FloatField(
        required=False,
        max_value=100.0,
        min_value=0.0,
    )

    class Meta:
        model = ExerciseApproachInWorkoutTemplate
        fields = '__all__'
        read_only_fields = ['id']


class ExerciseApproachInWorkoutTemplateOrderSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(
        required=True,
    )
    ordinal_number = serializers.IntegerField(
        required=True,
    )

    class Meta:
        model = ExerciseApproachInWorkoutTemplate
        fields = '__all__'
        read_only_fields = ['reps', 'absolute_weight',
                            'relative_weight', 'exercise_in_workout_template']


class ExerciseApproachInWorkoutTemplateReorderSerializer(serializers.Serializer):
    approaches = ExerciseApproachInWorkoutTemplateOrderSerializer(many=True)
    exercise_in_template = serializers.UUIDField()

    def validate(self, attrs):
        approaches = attrs['approaches']
        approaches_count = len(approaches)
        approaches_order_list = [False] * approaches_count

        for approaches_dict in approaches:
            ordinal_number = approaches_dict['ordinal_number']
            index = ordinal_number - 1
            if not 1 <= ordinal_number <= approaches_count or approaches_order_list[index]:
                raise ValidationError(
                    {'ordinal_number': 'Incorrect ordinal numbers were passed'})

            approaches_order_list[index] = True

        return super().validate(attrs)
