from django.test import TestCase
from django.db.utils import IntegrityError

from slugify import slugify

from exercise.models import Exercise, ExerciseCategory


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
