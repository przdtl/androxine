from django.test import TestCase
from django.db import IntegrityError
from django.contrib.auth import get_user_model

from workout_template.models import (
    WorkoutTemplate,
    ExerciseInWorkoutTemplate,
    ExerciseApproachInWorkoutTemplate
)
from workout_settings.models import UserWorkoutSettings
from exercise.models import Exercise, ExerciseCategory

UserModel = get_user_model()

default_username = 'user'
default_password = 'asdSsd4223_ssas42?'
default_email = 'test@test.com'


class WorkoutTemplateModelTestCases(TestCase):
    def setUp(self) -> None:
        self.user = UserModel.objects.create_user(
            username=default_username,
            email=default_email,
            password=default_password,
        )

    def test_workout_template_repr(self):
        template = WorkoutTemplate.objects.create(
            created_by=self.user,
            name='супер треня',
        )

        self.assertEqual(str(template), '[{}]{}'.format(
            template.created_by, template.name))

    def test_workout_template_unique_constraint_with_the_same_user(self):
        WorkoutTemplate.objects.create(
            created_by=self.user,
            name='супер треня',
        )
        with self.assertRaises(IntegrityError):
            WorkoutTemplate.objects.create(
                created_by=self.user,
                name='супер треня',
            )

    def test_workout_template_unique_constraint_with_different_user(self):
        another_user = UserModel.objects.create_user(
            username='another',
            email='r.sdasa@gmail.com',
            password=default_password
        )
        WorkoutTemplate.objects.create(
            created_by=self.user,
            name='супер треня',
        )
        try:
            WorkoutTemplate.objects.create(
                created_by=another_user,
                name='супер треня',
            )
        except (IntegrityError):
            self.fail(
                "WorkoutTemplate.objects.create raised IntegrityError unexpectedly!"
            )

    def test_workout_template_set_break_manually(self):
        template = WorkoutTemplate.objects.create(
            created_by=self.user,
            name='супер треня',
            break_between_approaches=150
        )

        self.assertEqual(template.break_between_approaches, 150)

    def test_workout_template_set_break_by_default(self):
        template = WorkoutTemplate.objects.create(
            created_by=self.user,
            name='супер треня',
        )

        self.assertEqual(template.break_between_approaches, 120)

    def test_workout_template_change_default_and_set_break_by_default(self):
        settings = UserWorkoutSettings.objects.get(user=self.user)
        settings.break_between_approaches = 200
        settings.save()

        template = WorkoutTemplate.objects.create(
            created_by=self.user,
            name='супер треня',
        )

        self.assertEqual(template.break_between_approaches, 200)


class ExerciseInWorkoutTemplateModelTestCases(TestCase):
    def setUp(self) -> None:
        self.user = UserModel.objects.create_user(
            username=default_username,
            email=default_email,
            password=default_password,
        )
        self.template = WorkoutTemplate.objects.create(
            created_by=self.user,
            name='тест треня',
        )
        self.nogi = ExerciseCategory.objects.create(
            name='ноги'
        )
        self.prised = Exercise.objects.create(
            category=self.nogi,
            name='присед'
        )

    def test_exercise_in_workout_template_repr(self):
        exercise_in_template = ExerciseInWorkoutTemplate.objects.create(
            template=self.template,
            exercise=self.prised,
        )

        self.assertEqual(
            str(exercise_in_template),
            '{}.{}'.format(exercise_in_template.template,
                           exercise_in_template.exercise)
        )

    def test_exercise_in_workout_template_unique_constraint_with_the_same_user(self):
        ExerciseInWorkoutTemplate.objects.create(
            template=self.template,
            exercise=self.prised,
        )
        with self.assertRaises(IntegrityError):
            ExerciseInWorkoutTemplate.objects.create(
                template=self.template,
                exercise=self.prised,
            )

    def test_exercise_in_workout_template_unique_constraint_with_different_user(self):
        another_template = WorkoutTemplate.objects.create(
            created_by=self.user,
            name='новая треня',
        )
        ExerciseInWorkoutTemplate.objects.create(
            template=self.template,
            exercise=self.prised,
        )
        try:
            ExerciseInWorkoutTemplate.objects.create(
                template=another_template,
                exercise=self.prised,
            )
        except (IntegrityError):
            self.fail(
                "ExerciseInWorkoutTemplate.objects.create raised IntegrityError unexpectedly!"
            )

    def test_exercise_in_workout_template_autocreate_ordinal_number(self):
        zhim = Exercise.objects.create(
            name='жим',
            category=self.nogi
        )
        vipad = Exercise.objects.create(
            name='выпады',
            category=self.nogi,
        )
        first = ExerciseInWorkoutTemplate.objects.create(
            template=self.template,
            exercise=self.prised,
        )
        second = ExerciseInWorkoutTemplate.objects.create(
            template=self.template,
            exercise=zhim,
        )
        third = ExerciseInWorkoutTemplate.objects.create(
            template=self.template,
            exercise=vipad,
        )
        self.assertEqual(first.ordinal_number, 1)
        self.assertEqual(second.ordinal_number, 2)
        self.assertEqual(third.ordinal_number, 3)

    def test_exercise_in_workout_template_create_ordinal_number_manually(self):
        zhim = Exercise.objects.create(
            name='жим',
            category=self.nogi,
        )
        vipad = Exercise.objects.create(
            name='выпады',
            category=self.nogi,
        )
        first = ExerciseInWorkoutTemplate.objects.create(
            template=self.template,
            exercise=self.prised,
            ordinal_number=4,
        )
        second = ExerciseInWorkoutTemplate.objects.create(
            template=self.template,
            exercise=zhim,
            ordinal_number=10,
        )
        third = ExerciseInWorkoutTemplate.objects.create(
            template=self.template,
            exercise=vipad,
            ordinal_number=7,
        )
        self.assertEqual(first.ordinal_number, 1)
        self.assertEqual(second.ordinal_number, 2)
        self.assertEqual(third.ordinal_number, 3)

    def test_change_ordinal_number_after_delete_exercise_in_workout_template_template(self):
        zhim = Exercise.objects.create(
            name='жим',
            category=self.nogi
        )
        vipad = Exercise.objects.create(
            name='выпады',
            category=self.nogi,
        )
        first = ExerciseInWorkoutTemplate.objects.create(
            template=self.template,
            exercise=self.prised,
        )
        second = ExerciseInWorkoutTemplate.objects.create(
            template=self.template,
            exercise=zhim,
        )
        third = ExerciseInWorkoutTemplate.objects.create(
            template=self.template,
            exercise=vipad,
        )
        second.delete()

        first.refresh_from_db()
        third.refresh_from_db()

        self.assertEqual(first.ordinal_number, 1)
        self.assertEqual(third.ordinal_number, 2)

        first.delete()

        third.refresh_from_db()

        self.assertEqual(third.ordinal_number, 1)


class ExerciseApproachInWorkoutTemplateModelTestCases(TestCase):
    def setUp(self) -> None:
        self.user = UserModel.objects.create_user(
            username=default_username,
            email=default_email,
            password=default_password,
        )
        self.template = WorkoutTemplate.objects.create(
            created_by=self.user,
            name='тест треня',
        )
        self.nogi = ExerciseCategory.objects.create(
            name='ноги'
        )
        self.prised = Exercise.objects.create(
            category=self.nogi,
            name='присед'
        )
        self.prised_in_template = ExerciseInWorkoutTemplate.objects.create(
            template=self.template,
            exercise=self.prised,
        )

    def test_approach_repr(self):
        approach = ExerciseApproachInWorkoutTemplate.objects.create(
            exercise_in_workout_template=self.prised_in_template,
            absolute_weight=115
        )

        self.assertEqual(
            str(approach), '{}.{}'.format(
                approach.exercise_in_workout_template, approach.ordinal_number)
        )

    def test_approach_autocreate_ordinal_number(self):
        first = ExerciseApproachInWorkoutTemplate.objects.create(
            exercise_in_workout_template=self.prised_in_template,
            absolute_weight=115
        )
        second = ExerciseApproachInWorkoutTemplate.objects.create(
            exercise_in_workout_template=self.prised_in_template,
            absolute_weight=130
        )
        third = ExerciseApproachInWorkoutTemplate.objects.create(
            exercise_in_workout_template=self.prised_in_template,
            absolute_weight=145
        )

        self.assertEqual(first.ordinal_number, 1)
        self.assertEqual(second.ordinal_number, 2)
        self.assertEqual(third.ordinal_number, 3)

    def test_approach_create_ordinal_number_manually(self):
        first = ExerciseApproachInWorkoutTemplate.objects.create(
            exercise_in_workout_template=self.prised_in_template,
            absolute_weight=115,
            ordinal_number=4,
        )
        second = ExerciseApproachInWorkoutTemplate.objects.create(
            exercise_in_workout_template=self.prised_in_template,
            absolute_weight=130,
            ordinal_number=5,
        )
        third = ExerciseApproachInWorkoutTemplate.objects.create(
            exercise_in_workout_template=self.prised_in_template,
            absolute_weight=145,
            ordinal_number=11,
        )

        self.assertEqual(first.ordinal_number, 1)
        self.assertEqual(second.ordinal_number, 2)
        self.assertEqual(third.ordinal_number, 3)

    def test_change_ordinal_number_after_delete_approach(self):
        first = ExerciseApproachInWorkoutTemplate.objects.create(
            exercise_in_workout_template=self.prised_in_template,
            absolute_weight=115
        )
        second = ExerciseApproachInWorkoutTemplate.objects.create(
            exercise_in_workout_template=self.prised_in_template,
            absolute_weight=130
        )
        third = ExerciseApproachInWorkoutTemplate.objects.create(
            exercise_in_workout_template=self.prised_in_template,
            absolute_weight=145
        )
        second.delete()

        first.refresh_from_db()
        third.refresh_from_db()

        self.assertEqual(first.ordinal_number, 1)
        self.assertEqual(third.ordinal_number, 2)

        first.delete()

        third.refresh_from_db()

        self.assertEqual(third.ordinal_number, 1)
