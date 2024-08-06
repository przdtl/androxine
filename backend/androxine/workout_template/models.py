from decimal import Decimal

from django.db import models
from django.db.models import F
from django.core.validators import MinValueValidator

from config.utils import current_timestamp_ulid


class WorkoutTemplate(models.Model):
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
    name = models.CharField(
        max_length=255,
    )
    break_between_approaches = models.PositiveSmallIntegerField()

    def __str__(self) -> str:
        return '[{}]{}'.format(self.created_by, self.name)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['created_by', 'name'],
                name='unique template name for every user')
        ]


class ExerciseInWorkoutTemplate(models.Model):
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        default=current_timestamp_ulid,
    )
    template = models.ForeignKey(
        'WorkoutTemplate',
        on_delete=models.CASCADE,
        related_name='exercises'
    )
    exercise = models.ForeignKey(
        'exercise.Exercise',
        on_delete=models.CASCADE,
    )
    ordinal_number = models.SmallIntegerField(
        default=1,
        unique=True,
        editable=False,
        validators=[MinValueValidator(1)]
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['exercise', 'template'],
                name='unique exercise for every template')
        ]

    def __str__(self) -> str:
        return '{}.{}'.format(self.template, self.exercise)

    def save(self, *args, **kwargs) -> None:
        is_present = bool(self.__class__.objects.filter(pk=self.pk))
        if not is_present:
            approaches_count = self.__class__.objects.filter(
                template=self.template,
            ).count()
            self.ordinal_number = approaches_count + 1

        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        queryset = self.__class__.objects.filter(
            template=self.template,
            ordinal_number__gt=self.ordinal_number
        )
        deleted_item = super().delete(*args, **kwargs)
        queryset.update(
            ordinal_number=F('ordinal_number') - 1
        )

        return deleted_item


class ExerciseApproachInWorkoutTemplate(models.Model):
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        default=current_timestamp_ulid,
    )
    exercise_in_workout_template = models.ForeignKey(
        'ExerciseInWorkoutTemplate',
        on_delete=models.CASCADE,
        related_name='approaches',
    )
    relative_weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('000.00'))]
    )
    absolute_weight = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0)]
    )
    reps = models.PositiveIntegerField(
        default=0,
    )
    ordinal_number = models.SmallIntegerField(
        default=1,
        unique=True,
        editable=False,
        validators=[MinValueValidator(1)]
    )

    def __str__(self) -> str:
        return '{}.{}'.format(self.exercise_in_workout_template, self.ordinal_number)

    def save(self, *args, **kwargs) -> None:
        is_present = bool(self.__class__.objects.filter(pk=self.pk))
        if not is_present:
            approaches_count = self.__class__.objects.filter(
                exercise_in_workout_template=self.exercise_in_workout_template
            ).count()
            self.ordinal_number = approaches_count + 1

        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        queryset = self.__class__.objects.filter(
            exercise_in_workout_template=self.exercise_in_workout_template,
            ordinal_number__gt=self.ordinal_number
        )
        deleted_item = super().delete(*args, **kwargs)
        queryset.update(
            ordinal_number=F('ordinal_number') - 1
        )

        return deleted_item
