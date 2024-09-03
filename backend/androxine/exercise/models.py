from django.db import models

from autoslug import AutoSlugField

from config.utils import current_timestamp_ulid


class ExerciseCategory(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
    )
    slug = AutoSlugField(
        max_length=255,
        blank=True,
        unique=True,
        populate_from='name',
        always_update=True,
    )

    def __str__(self) -> str:
        return self.name


class Exercise(models.Model):
    name = models.CharField(
        max_length=255,
    )
    slug = AutoSlugField(
        max_length=255,
        blank=True,
        unique=True,
        populate_from='name',
        always_update=True,
    )
    category = models.ForeignKey(
        'ExerciseCategory',
        on_delete=models.CASCADE
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'category'],
                name='Exercise names must be unique for every category')
        ]

    def __str__(self) -> str:
        return '[{}]{}'.format(self.category, self.name)


class UserExerciseSettings(models.Model):
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        default=current_timestamp_ulid,
    )
    user = models.ForeignKey(
        'authenticate.user',
        on_delete=models.CASCADE,
    )
    exercise = models.ForeignKey(
        'Exercise',
        on_delete=models.CASCADE,
    )
    one_time_maximum = models.FloatField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'exercise'],
                name='unique exercise for every user')
        ]

    def __str__(self) -> str:
        return '[{}].{}'.format(self.user, self.exercise)
