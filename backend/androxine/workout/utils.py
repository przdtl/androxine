import uuid

from exercise.models import UserExerciseSettings

from workout_template.models import ExerciseApproachInWorkoutTemplate

from workout.models import Workout


def calculate_absolute_weight_from_relative(template_approach_id: uuid.UUID) -> float:
    try:
        template_approach = ExerciseApproachInWorkoutTemplate.objects.get(
            pk=template_approach_id,
            relative_weight__isnull=False,
        )
    except ExerciseApproachInWorkoutTemplate.DoesNotExist:
        raise ValueError('Invalid template_approach_id value')

    user = template_approach.exercise_in_workout_template.template.created_by
    exercise = template_approach.exercise_in_workout_template.exercise

    try:
        user_exercise_settings = UserExerciseSettings.objects.get(
            user=user,
            exercise=exercise,
        )
    except UserExerciseSettings.DoesNotExist:
        raise ValueError(
            'UserExerciseSettings instance for this user and exrcise does not exists'
        )

    one_time_maximum = user_exercise_settings.one_time_maximum
    percentage = float(template_approach.relative_weight)

    return round(one_time_maximum * percentage, 2)


def is_exists_non_finished_workout() -> bool:
    return Workout.objects.filter(
        enging_datetime__isnull=True
    ).exists()
