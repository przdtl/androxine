from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from config.utils import delete_cache

from exercise.models import Exercise, ExerciseCategory


@receiver(post_delete, sender=ExerciseCategory, dispatch_uid='exercise_category_post_deleted')
def exercise_category_post_delete_handler(sender, **kwargs):
    delete_cache(ExerciseCategory.__name__)


@receiver(post_save, sender=ExerciseCategory, dispatch_uid='exercise_category_post_saved')
def exercise_category_post_save_handler(sender, **kwargs):
    delete_cache(ExerciseCategory.__name__)


@receiver(post_delete, sender=Exercise, dispatch_uid='exercise_post_deleted')
def exercise_post_delete_handler(sender, **kwargs):
    delete_cache(Exercise.__name__)


@receiver(post_save, sender=Exercise, dispatch_uid='exercise_post_saved')
def exercise_post_save_handler(sender, **kwargs):
    delete_cache(Exercise.__name__)
