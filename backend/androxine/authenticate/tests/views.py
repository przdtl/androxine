from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.test.utils import override_settings

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.exceptions import NotAuthenticated

from authenticate.serializers import (
    SignupSerializer,
    SigninSerializer,
    UserReadSerializer,
)
from authenticate.services import EmailVerificationTokenGenerator

UserModel = get_user_model()


@override_settings(
    EMAIL_BACKEND='django.core.mail.backends.console.EmailBackend',
    CELERY_BROKER_URL='memory://localhost/',
)
class UserRegisterTest(APITestCase):
    def setUp(self) -> None:
        self.url = reverse_lazy('signup')

    def test_signup_valid_user(self):
        user_data = {
            'username': 'user',
            'email': 'test.test_user@gmail.com',
            'password': '23fcf453DSdhej#_d',
            'password2': '23fcf453DSdhej#_d',
        }
        response = self.client.post(self.url, user_data)

        user = UserModel.objects.get(pk=response.data.get('id'))
        user.delete()

        serializer = SignupSerializer(data=user_data)
        serializer.is_valid()
        serializer.save()

        response_data = response.data
        del response_data['id']

        serializer_data = serializer.data
        del serializer_data['id']

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_data, serializer_data)

    def test_signup_with_weak_password(self):
        user_data = {
            'username': 'user',
            'email': 'test.test_user@gmail.com',
            'password': '1111',
            'password2': '1111',
        }
        response = self.client.post(self.url, user_data)
        serializer = SignupSerializer(data=user_data)
        serializer.is_valid()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, serializer.errors)

    def test_signup_with_mismatched_passwords(self):
        user_data = {
            'username': 'user',
            'email': 'test.test_user@gmail.com',
            'password': '15d7rBOdN>{Uc~F',
            'password2': '7>B~Q"[02`/EE5w',
        }
        response = self.client.post(self.url, user_data)
        serializer = SignupSerializer(data=user_data)
        serializer.is_valid()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, serializer.errors)

    def test_signup_with_already_existed_email(self):
        email = 'test.test_user@gmail.com'

        UserModel.objects.create_user(
            username='user1',
            email=email,
            password='7>B~Q"[02`/EE5w'
        )

        user_data = {
            'username': 'user2',
            'email': email,
            'password': '15d7rBOdN>{Uc~F',
            'password2': '15d7rBOdN>{Uc~F',
        }
        response = self.client.post(self.url, user_data)
        serializer = SignupSerializer(data=user_data)
        serializer.is_valid()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, serializer.errors)

    def test_signup_with_already_existed_username(self):
        username = 'user'

        UserModel.objects.create_user(
            username=username,
            email='test1.test_user@gmail.com',
            password='7>B~Q"[02`/EE5w'
        )

        user_data = {
            'username': username,
            'email': 'test2.test_user@gmail.com',
            'password': '15d7rBOdN>{Uc~F',
            'password2': '15d7rBOdN>{Uc~F',
        }
        response = self.client.post(self.url, user_data)
        serializer = SignupSerializer(data=user_data)
        serializer.is_valid()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, serializer.errors)


class ActivateUserTest(APITestCase):
    def setUp(self) -> None:
        self.user = UserModel.objects.create_user(
            username='user',
            email='user.user@gmail.com',
            password='asdSsd4223_ssas42?',
        )
        self.user.is_active = True
        self.user.save()

    def test_activate_active_existed_user(self):
        token = EmailVerificationTokenGenerator().make_token(self.user)
        url = reverse_lazy('activate', args=[self.user.pk, token])
        response = self.client.get(url)
        expected_data = {'detail': _('User is already active')}

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_data)

    def test_activate_non_active_existed_user(self):
        token = EmailVerificationTokenGenerator().make_token(self.user)
        self.user.is_active = False
        self.user.save()
        url = reverse_lazy('activate', args=[self.user.pk, token])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, None)

    def test_activate_non_existed_user(self):
        token = EmailVerificationTokenGenerator().make_token(self.user)
        uid = self.user.pk
        self.user.delete()
        url = reverse_lazy('activate', args=[uid, token])
        response = self.client.get(url)
        expected_data = {'detail': _('Token is invalid')}

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, expected_data)


class UserLoginTest(APITestCase):
    def setUp(self) -> None:
        self.url = reverse_lazy('signin')
        self.user = UserModel.objects.create_user(
            username='user',
            email='test1.test_user@gmail.com',
            password='7>B~Q"[02`/EE5w'
        )

    def test_signin_active_valid_user_by_username(self):
        user_data = {
            'username': 'user',
            'password': '7>B~Q"[02`/EE5w',
        }
        response = self.client.post(self.url, user_data)

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(response.data, None)

    def test_signin_active_valid_user_by_email(self):
        user_data = {
            'username': 'test1.test_user@gmail.com',
            'password': '7>B~Q"[02`/EE5w',
        }
        response = self.client.post(self.url, user_data)

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(response.data, None)

    def test_signin_non_active_valid_user(self):
        self.user.is_active = False
        self.user.save()

        user_data = {
            'username': 'user',
            'password': '7>B~Q"[02`/EE5w',
        }
        response = self.client.post(self.url, user_data)
        serializer = SigninSerializer(data=user_data)
        serializer.is_valid()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, serializer.errors)

    def test_signin_active_non_valid_password(self):
        user_data = {
            'username': 'user',
            'password': '1111',
        }
        response = self.client.post(self.url, user_data)
        serializer = SigninSerializer(data=user_data)
        serializer.is_valid()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, serializer.errors)


class UserProfileTest(APITestCase):
    def setUp(self) -> None:
        self.url = reverse_lazy('me')
        self.username = 'user'
        self.email = 'user@test.com'
        self.password = '7>B~Q"[02`/EE5w'
        self.user = UserModel.objects.create_user(
            self.username,
            self.email,
            self.password,
        )

    def test_getting_profile_of_logged_in_user(self):
        self.assertTrue(self.client.login(
            username=self.username, password=self.password)
        )

        response = self.client.get(self.url)

        serializer_data = UserReadSerializer({
            'id': self.user.pk,
            'username': self.username,
            'email': self.email,
        }).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer_data)

    def test_getting_profile_of_not_logged_in_user(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data, {'detail': NotAuthenticated.default_detail})


class UserLogoutTest(APITestCase):
    def setUp(self) -> None:
        self.url = reverse_lazy('signout')
        self.username = 'user'
        self.email = 'user@test.com'
        self.password = '7>B~Q"[02`/EE5w'
        self.user = UserModel.objects.create_user(
            self.username,
            self.email,
            self.password,
        )

    def test_signout_of_logged_in_user(self):
        self.assertTrue(self.client.login(
            username=self.username, password=self.password)
        )

        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, None)

    def test_signout_of_not_logged_in_user(self):
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data, {'detail': NotAuthenticated.default_detail}
        )
