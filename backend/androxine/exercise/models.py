from django.db import models
from autoslug import AutoSlugField


class ExerciseCategory(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
    )
    slug = AutoSlugField(
        max_length=255,
        blank=True,
        populate_from='name',
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
