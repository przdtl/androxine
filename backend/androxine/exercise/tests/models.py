from django.test import TestCase
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model

from slugify import slugify

from exercise.models import Exercise, ExerciseCategory, UserExerciseSettings

UserModel = get_user_model()


class ExerciseCategoryTest(TestCase):
    def setUp(self) -> None:
        ExerciseCategory.objects.create(name='ноги')

    def test_unique_category_name(self):
        with self.assertRaises(IntegrityError):
            ExerciseCategory.objects.create(name='ноги')

    def test_str_representation(self):
        category = ExerciseCategory.objects.first()

        self.assertEqual(str(category), 'ноги')


class ExerciseTest(TestCase):
    def setUp(self) -> None:
        self.nogi = ExerciseCategory.objects.create(name='ноги')
        self.grud = ExerciseCategory.objects.create(name='грудь')

        nogi_exercises = ['присед', 'жим']
        grud_exercises = ['разводка', 'бабочка']

        Exercise.objects.bulk_create(
            [Exercise(name=name, category_id=self.nogi.pk) for name in nogi_exercises])

        Exercise.objects.bulk_create(
            [Exercise(name=name, category_id=self.grud.pk) for name in grud_exercises])

    def test_add_exercise_with_existing_name_in_same_category(self):
        with self.assertRaises(IntegrityError):
            Exercise.objects.create(name='жим', category_id=self.nogi.pk)

    def test_add_exercise_withexisting_name_in_other_category(self):
        try:
            Exercise.objects.create(name='жим', category_id=self.grud.pk)
        except Exception:
            self.fail(
                'test_add_exercise_withexisting_name_in_other_category raised an exception')

    def test_str_representation(self):
        prised_exercise = Exercise.objects.get(
            name='присед', category=self.nogi
        )

        self.assertEqual(str(prised_exercise),
                         '[{}]{}'.format('ноги', 'присед'))

    def test_slugify_exercise_name(self):
        prised_exercise = Exercise.objects.get(
            name='присед', category=self.nogi
        )

        self.assertEqual(prised_exercise.slug, slugify('присед'))


class UserExerciseSettingsTest(TestCase):
    def setUp(self) -> None:
        self.nogi = ExerciseCategory.objects.create(name='ноги')
        self.prised = Exercise.objects.create(
            name='присед', category_id=self.nogi.pk)
        self.user = UserModel.objects.create_user(
            username='user',
            email='user.user@gmail.com',
            password='asdSsd4223_ssas42?',
        )
        UserExerciseSettings.objects.create(
            user_id=self.user.pk,
            exercise_id=self.prised.pk,
            one_time_maximum=66,
        )

    def test_str_representation(self):
        prised_settings = UserExerciseSettings.objects.get(
            user_id=self.user.pk,
            exercise_id=self.prised.pk,
        )

        self.assertEqual(str(prised_settings),
                         '[{}]{}'.format(str(self.user), str(self.prised)))
