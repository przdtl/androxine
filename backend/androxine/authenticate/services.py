from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator

UserModel = get_user_model()


class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    pass


def get_user_from_email_verification_token(user_id, token):
    try:
        user = UserModel.objects.get(pk=user_id)
    except UserModel.DoesNotExist:
        return None

    if EmailVerificationTokenGenerator().check_token(user, token):
        return user
