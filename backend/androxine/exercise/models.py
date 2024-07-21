from django.db import models
from django.utils.text import slugify


class ExerciseCategory(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
    )
    slug = models.SlugField(
        max_length=255,
        blank=True,
    )

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

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
