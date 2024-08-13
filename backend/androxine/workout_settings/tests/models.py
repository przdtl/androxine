from django.test import TestCase
from django.contrib.auth import get_user_model

from workout_settings.models import UserWorkoutSettings

UserModel = get_user_model()


class UserWorkoutSettingsModelTestCase(TestCase):
    def setUp(self) -> None:
        self.user = UserModel.objects.create_user(
            username='user',
            email='test@test.com',
            password='asdSsd4223_ssas42?',
        )

    def test_user_workout_settings_create_after_user_creation(self) -> None:
        try:
            UserWorkoutSettings.objects.get(user_id=self.user.id)
        except (UserWorkoutSettings.DoesNotExist, UserWorkoutSettings.MultipleObjectsReturned):
            self.fail(
                "UserWorkoutSettings.objects.get(user_id=self.user.id) raised DoesNotExist or MultipleObjectsReturned unexpectedly!"
            )

    def test_user_workout_settings_representation(self) -> None:
        instance = UserWorkoutSettings.objects.get(user_id=self.user.id)

        self.assertEqual(str(instance), str(instance.user))
