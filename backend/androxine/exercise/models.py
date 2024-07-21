from django.db import models
from pytils.translit import slugify


class ExerciseCategory(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
    )
    slug = models.SlugField(
        max_length=255,
        blank=True,
    )

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Exercise(models.Model):
    name = models.CharField(
        max_length=255,
    )
    category = models.ForeignKey(
        'ExerciseCategory',
        on_delete=models.CASCADE
    )
    slug = models.SlugField(
        max_length=255,
        blank=True,
    )

    class Meta:
        unique_together = ['name', 'category']

    def __str__(self) -> str:
        return '[{}]{}'.format(self.category, self.name)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
