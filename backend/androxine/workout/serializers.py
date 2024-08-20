from rest_framework import serializers

from workout_template.models import ExerciseApproachInWorkoutTemplate
from workout.models import Workout, ExerciseInWorkout, ExerciseApproachInWorkout


class WorkoutReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = '__all__'
        read_only_fields = ['id']


class WorkoutCreateSwaggerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = ['break_between_approaches']


class WorkoutCreateByTemplateSerializer(serializers.ModelSerializer):
    break_between_approaches = serializers.IntegerField(
        source='workout_template__break_between_approaches',
    )

    class Meta:
        model = Workout
        fields = '__all__'
        read_only_fields = ['id']


class WorkoutCreateByTemplateSwaggerSerializer(serializers.ModelSerializer):
    workout_template = serializers.UUIDField(
        required=True,
    )

    class Meta:
        model = Workout
        fields = ['workout_template']


class WorkoutIsOverSwaggerSerializer(serializers.Serializer):
    is_over_only = serializers.BooleanField(
        required=False,
        default=True,
    )


class ExerciseApproachInWorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseApproachInWorkout
        fields = '__all__'
        read_only_fields = ['id', 'datetime']


class ApproachByTemplateSwaggerSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(
        required=True,
    )

    class Meta:
        model = ExerciseApproachInWorkoutTemplate
        fields = ['id']


class WorkoutIdSwaggerSerializer(serializers.ModelSerializer):
    workout_id = serializers.UUIDField(
        source='id',
        required=True,
    )

    class Meta:
        model = Workout
        fields = ['workout_id']


class ExerciseInWorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseInWorkout
        fields = '__all__'


class ExerciseInWorkoutCreateSwaggerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseInWorkout
        fields = ['exercise']
