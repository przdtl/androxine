import uuid

from typing import Optional, Any

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator

UserModel = get_user_model()


class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    '''
    Token generator for user verification via email after registration
    '''


def get_user_from_email_verification_token(user_id: uuid.UUID, token: str) -> Optional[Any]:
    '''
    Email verification token validator

    Args:
        user_id (uuid.UUID): user primary key
        token (str): email verification token required for validation

    Returns:
        Optional[UserModel]: user instance is token is valid and None otherwise
    '''
    try:
        user = UserModel.objects.get(pk=user_id)
    except UserModel.DoesNotExist:
        return None

    if EmailVerificationTokenGenerator().check_token(user, token):
        return user
