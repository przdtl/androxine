from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test.utils import override_settings

from authenticate.services import (
    get_user_from_email_verification_token,
    EmailVerificationTokenGenerator,
)

UserModel = get_user_model()


@override_settings(
    EMAIL_BACKEND='django.core.mail.backends.console.EmailBackend',
    CELERY_BROKER_URL='memory://localhost/',
)
class EmailVerificationTokenTest(TestCase):
    def setUp(self) -> None:
        self.user = UserModel.objects.create_user(
            username='user',
            email='user.user@gmail.com',
            password='asdSsd4223_ssas42?',
        )

    def test_inactive_user_with_valid_token(self):
        inactive_user = self.user
        token = EmailVerificationTokenGenerator().make_token(inactive_user)
        active_user = get_user_from_email_verification_token(
            inactive_user.pk,
            token
        )

        self.assertEqual(inactive_user, active_user)

    def test_inactive_user_with_invalid_token(self):
        inactive_user = self.user
        token = 'sdfsdfsdfsdfsdfsdfsdfsdfsdf'
        active_user = get_user_from_email_verification_token(
            inactive_user.pk,
            token
        )

        self.assertIsNone(active_user)

    def test_inactive_user_with_valid_token_from_other_inactive_user(self):
        inactive_user = self.user
        other_user = UserModel.objects.create_user(
            username='other_user',
            email='other.other@gmail.com',
            password='asdSsd4223_ssas42?',
        )
        token = EmailVerificationTokenGenerator().make_token(other_user)
        active_user = get_user_from_email_verification_token(
            inactive_user.pk,
            token
        )

        self.assertIsNone(active_user)

    def test_active_user_with_valid_token(self):
        active_user = self.user
        token = EmailVerificationTokenGenerator().make_token(active_user)
        user = get_user_from_email_verification_token(
            active_user.pk,
            token
        )

        self.assertEqual(active_user, user)

    def test_non_existing_user_with_valid_token(self):
        user = self.user
        token = EmailVerificationTokenGenerator().make_token(user)
        user.delete()
        user = get_user_from_email_verification_token(
            user.pk,
            token
        )

        self.assertIsNone(user)

    def test_non_existing_user_with_invalid_token(self):
        user = self.user
        token = 'sdfsdfsdfsdfsdfsdfsdfsdfsdf'
        user.delete()
        user = get_user_from_email_verification_token(
            user.pk,
            token
        )

        self.assertIsNone(user)
