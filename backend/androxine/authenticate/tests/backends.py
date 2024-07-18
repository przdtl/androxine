from django.test import TestCase
from django.http import HttpRequest
from django.contrib.auth import get_user_model

from authenticate.backends import EmailUsernameModelBackend

UserModel = get_user_model()


class EmailUsernameModelBackendTest(TestCase):
    def setUp(self) -> None:
        self.user = UserModel.objects.create_user(
            username='user',
            email='user.user@gmail.com',
            password='asdSsd4223_ssas42?',
        )

    def test_authenticate_with_valid_username_and_password(self):
        username = 'user'
        password = 'asdSsd4223_ssas42?'

        backend = EmailUsernameModelBackend()
        user = backend.authenticate(HttpRequest(), username, password)

        self.assertEqual(self.user, user)

    def test_authenticate_with_valid_email_and_password(self):
        username = 'user.user@gmail.com'
        password = 'asdSsd4223_ssas42?'

        backend = EmailUsernameModelBackend()
        user = backend.authenticate(HttpRequest(), username, password)

        self.assertEqual(self.user, user)

    def test_authenticate_user_with_valid_username_and_invalid_password(self):
        username = 'user'
        password = 'dsdsdsd'

        backend = EmailUsernameModelBackend()
        user = backend.authenticate(HttpRequest(), username, password)

        self.assertIsNone(user)

    def test_authenticate_user_with_invalid_username_and_valid_password(self):
        username = 'not_user'
        password = 'asdSsd4223_ssas42?'

        backend = EmailUsernameModelBackend()
        user = backend.authenticate(HttpRequest(), username, password)

        self.assertIsNone(user)

    def test_authenticate_user_with_invalid_username_and_invalid_password(self):
        username = 'not_user'
        password = 'dsdsdsd'

        backend = EmailUsernameModelBackend()
        user = backend.authenticate(HttpRequest(), username, password)

        self.assertIsNone(user)

    def test_authenticate_user_by_none_username(self):
        username = None
        password = 'dsdsdsd'

        backend = EmailUsernameModelBackend()
        user = backend.authenticate(HttpRequest(), username, password)

        self.assertIsNone(user)

    def test_authenticate_user_by_none_password(self):
        username = 'user'
        password = None

        backend = EmailUsernameModelBackend()
        user = backend.authenticate(HttpRequest(), username, password)

        self.assertIsNone(user)
