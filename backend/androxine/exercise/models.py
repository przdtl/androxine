from django.db import models
from autoslug import AutoSlugField


class ExerciseCategory(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
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
    )
    category = models.ForeignKey(
        'ExerciseCategory',
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ['name', 'category']

    def __str__(self) -> str:
        return '[{}]{}'.format(self.category, self.name)


class UserExerciseSettings(models.Model):
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
