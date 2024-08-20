from django.db import models
from django.core.validators import MinValueValidator

from config.utils import current_timestamp_ulid

from workout_settings.models import UserWorkoutSettings


class Workout(models.Model):
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        default=current_timestamp_ulid,
    )
    created_by = models.ForeignKey(
        'authenticate.user',
        on_delete=models.CASCADE,
    )
    beginning_datetime = models.DateTimeField(
        auto_now_add=True,
    )
    enging_datetime = models.DateTimeField(
        null=True,
        blank=True,
    )
    break_between_approaches = models.PositiveSmallIntegerField(
        blank=True,
    )
    workout_template = models.ForeignKey(
        'workout_template.workouttemplate',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return '[{}]{}'.format(self.created_by, self.beginning_datetime) + (' - {}'.format(self.enging_datetime) if self.enging_datetime else '')

    def save(self, *args, **kwargs) -> None:
        if not self.break_between_approaches:
            if self.workout_template:
                self.break_between_approaches = self.workout_template.break_between_approaches
            else:
                settings = UserWorkoutSettings.objects.get(
                    user=self.created_by
                )
                self.break_between_approaches = settings.break_between_approaches

        return super().save(*args, **kwargs)


class ExerciseInWorkout(models.Model):
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        default=current_timestamp_ulid,
    )
    workout = models.ForeignKey(
        'workout',
        on_delete=models.CASCADE,
        related_name='exercises'
    )
    exercise = models.ForeignKey(
        'exercise.Exercise',
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return '{}.{}'.format(self.workout, self.exercise)


class ExerciseApproachInWorkout(models.Model):
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        default=current_timestamp_ulid,
    )
    exercise_in_workout = models.ForeignKey(
        'ExerciseInWorkout',
        on_delete=models.CASCADE,
        related_name='approaches',
    )
    weight = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0)]
    )
    reps = models.PositiveIntegerField(
        default=0,
    )
    datetime = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self) -> str:
        return '{}[{}]'.format(self.exercise_in_workout, self.datetime)
