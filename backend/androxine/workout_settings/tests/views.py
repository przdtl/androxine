from django.urls import reverse_lazy
from django.forms.models import model_to_dict
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.exceptions import NotAuthenticated

from workout_settings.models import UserWorkoutSettings
from workout_settings.serializers import UserWorkoutSettingsSerializer

UserModel = get_user_model()


class GETUserWorkoutSettingsViewTestCase(APITestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.url = reverse_lazy('workout_settings')

    def setUp(self) -> None:
        self.user = UserModel.objects.create_user(
            username='user',
            email='test@test.com',
            password='asdSsd4223_ssas42?',
        )
        self.client.login(
            username='user',
            password='asdSsd4223_ssas42?',
        )

    def test_get_user_workout_settings_by_non_logging_user(self):
        self.client.logout()
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data, {'detail': NotAuthenticated.default_detail}
        )

    def test_get_user_workout_settings_by_logging_user(self):
        response = self.client.get(self.url)
        instance = UserWorkoutSettings.objects.get(user_id=self.user.id)
        serializer_data = UserWorkoutSettingsSerializer(instance).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer_data)


class PUTUserWorkoutSettingsViewTestCase(APITestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.url = reverse_lazy('workout_settings')

    def setUp(self) -> None:
        self.user = UserModel.objects.create_user(
            username='user',
            email='test@test.com',
            password='asdSsd4223_ssas42?',
        )
        self.client.login(
            username='user',
            password='asdSsd4223_ssas42?',
        )

    def test_put_user_workout_settings_by_non_logging_user(self):
        self.client.logout()
        response = self.client.put(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data, {'detail': NotAuthenticated.default_detail}
        )

    def test_put_user_workout_settings(self):
        request_body = {
            'break_between_approaches': 200,
        }
        response = self.client.put(self.url, request_body)

        instance = UserWorkoutSettings.objects.get(user_id=self.user.id)
        serializer_data = UserWorkoutSettingsSerializer(instance).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer_data)


class PATCHUserWorkoutSettingsViewTestCase(APITestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.url = reverse_lazy('workout_settings')

    def setUp(self) -> None:
        self.user = UserModel.objects.create_user(
            username='user',
            email='test@test.com',
            password='asdSsd4223_ssas42?',
        )
        self.client.login(
            username='user',
            password='asdSsd4223_ssas42?',
        )

    def test_patch_user_workout_settings_by_non_logging_user(self):
        self.client.logout()
        response = self.client.patch(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data, {'detail': NotAuthenticated.default_detail}
        )

    def test_patch_user_workout_settings_all_fields(self):
        request_body = {
            'break_between_approaches': 200,
        }
        response = self.client.patch(self.url, request_body)
        instance = UserWorkoutSettings.objects.get(user_id=self.user.id)
        serializer_data = UserWorkoutSettingsSerializer(instance).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer_data)

    def test_patch_user_workout_settings_no_one_field(self):
        request_body = {}
        response = self.client.patch(self.url, request_body)
        instance = UserWorkoutSettings.objects.get(user_id=self.user.id)
        serializer_data = UserWorkoutSettingsSerializer(instance).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer_data)


class ResetUserWorkoutSettingsViewTestCase(APITestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.url = reverse_lazy('reset_workout_settings')

    def setUp(self) -> None:
        self.user = UserModel.objects.create_user(
            username='user',
            email='test@test.com',
            password='asdSsd4223_ssas42?',
        )
        self.client.login(
            username='user',
            password='asdSsd4223_ssas42?',
        )

    def test_reset_user_workout_settings_by_non_logging_user(self):
        self.client.logout()
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data, {'detail': NotAuthenticated.default_detail}
        )

    def test_reset_user_workout_settings(self):
        response = self.client.post(self.url)
        instance = UserWorkoutSettings.objects.get(user_id=self.user.id)
        serializer_data = UserWorkoutSettingsSerializer(instance).data
        new_instance = UserWorkoutSettings.objects.get(user_id=self.user.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer_data)
        self.assertEqual(serializer_data, model_to_dict(new_instance))
