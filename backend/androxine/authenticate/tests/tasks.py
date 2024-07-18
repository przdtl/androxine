from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test.utils import override_settings

from authenticate.tasks import send_user_verifications_email

UserModel = get_user_model()


@override_settings(
    EMAIL_BACKEND='django.core.mail.backends.console.EmailBackend',
    CELERY_BROKER_URL='memory://localhost/',
)
class SendUserVerificationEmailTests(TestCase):
    def setUp(self) -> None:
        self.user = UserModel.objects.create_user(
            username='user',
            email='user.user@gmail.com',
            password='asdSsd4223_ssas42?',
        )

    def test_send_email_for_existing_user(self):
        is_sent = send_user_verifications_email.apply(
            args=(self.user.pk, 'domain')).get()

        self.assertTrue(is_sent)

    def test_send_email_for_non_existent_user(self):
        user = self.user
        user.delete()

        is_sent = send_user_verifications_email.apply(
            args=(user.pk, 'domain')).get()

        self.assertFalse(is_sent)
