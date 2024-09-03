from typing import Any

from django.db.models import Q
from django.http import HttpRequest
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.base_user import AbstractBaseUser

UserModel = get_user_model()


class EmailUsernameModelBackend(ModelBackend):
    '''
    Overriding base backend for authenticate with username or email
    '''

    def authenticate(self, request: HttpRequest, username: str | None = ..., password: str | None = ..., **kwargs: Any) -> AbstractBaseUser | None:
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        if username is None or password is None:
            return
        try:
            user = UserModel.objects.get(
                Q(username__iexact=username) | Q(email__iexact=username))
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
            return
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
