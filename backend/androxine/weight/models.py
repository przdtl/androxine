import datetime

from django.db import models

from config.utils import current_timestamp_ulid


class Weight(models.Model):
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
    date = models.DateField(
        default=datetime.date.today
    )
    body_weight = models.FloatField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'date'],
                name='Weight records should be unique for each user per day')
        ]

    def __str__(self) -> str:
        return '[{}]{}'.format(self.user, self.date)

    def save(self, *args, **kwargs) -> None:
        try:
            today_weight = self.__class__.objects.get(
                date=datetime.date.today())
        except self.__class__.DoesNotExist:
            pass
        else:
            today_weight.delete()

        return super().save(*args, **kwargs)
