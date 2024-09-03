import uuid
import logging

from typing import Optional, Any

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator

logger = logging.getLogger(__name__)
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
        logger.info(
            'It is impossible to verify a user with id {}, as it does not exist'.format(
                user_id
            ))
        return None

    if EmailVerificationTokenGenerator().check_token(user, token):
        logger.info('The user with id {} has been successfully verified'.format(
            user_id
        ))
        return user

    logger.info(
        'It is impossible to verify a user with id {} because the token is invalid'.format(
            user_id
        ))
