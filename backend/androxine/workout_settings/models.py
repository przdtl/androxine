from django.db import models
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save

UserModel = get_user_model()


class UserWorkoutSettings(models.Model):
    user = models.OneToOneField(
        'authenticate.user',
        on_delete=models.CASCADE,
        related_name='workout_settings',
        primary_key=True
    )
    break_between_approaches = models.PositiveSmallIntegerField(
        default=120,
    )

    def __str__(self) -> str:
        return '{}'.format(self.user)


@receiver(post_save, sender=UserModel)
def create_workout_settings(sender, instance, created, **kwargs):
    if created:
        UserWorkoutSettings.objects.create(user=instance)
