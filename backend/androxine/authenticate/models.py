from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from config.utils import current_timestamp_ulid


class User(AbstractUser):
    id = models.UUIDField(
        primary_key=True,
        default=current_timestamp_ulid,
        editable=False,
    )

    first_name = None
    last_name = None

    email = models.EmailField(
        _("email address"),
        unique=True,
    )
