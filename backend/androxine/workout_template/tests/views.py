import uuid

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.exceptions import NotAuthenticated, ErrorDetail

from django.urls import reverse_lazy
from django.contrib.auth import get_user_model

from workout_template.models import (
    WorkoutTemplate,
    ExerciseInWorkoutTemplate,
    # ExerciseApproachInWorkoutTemplate
)
from workout_template.serializers import (
    WorkoutTemplateListCreateSerializer,
    # WorkoutTemplateReadSerializer,
    # ExerciseInWorkoutTemplateWriteSerializer,
    # ExerciseInWorkoutTemplateReadSerializer,
    # ExerciseApproachInWorkoutTemplateWriteSerializer,
    # ExerciseApproachInWorkoutTemplateReadSerializer,
)
from exercise.models import Exercise, ExerciseCategory

UserModel = get_user_model()

default_username = 'user'
default_password = 'asdSsd4223_ssas42?'
default_email = 'test@test.com'


class LISTWorkoutTemplateViewTestCases(APITestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.url = reverse_lazy('create_and_list_templates')

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
        self.client.login(
            username=default_username,
            password=default_password
        )

    def test_list_workout_template_by_non_logging_user(self):
        self.client.logout()
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data, {'detail': NotAuthenticated.default_detail}
        )


class POSTWorkoutTemplateViewTestCases(APITestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.url = reverse_lazy('create_and_list_templates')

    def setUp(self) -> None:
        self.user = UserModel.objects.create_user(
            username=default_username,
            email=default_email,
            password=default_password,
        )
        self.client.login(
            username=default_username,
            password=default_password
        )

    def test_post_workout_template_by_non_logging_user(self):
        self.client.logout()
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data, {'detail': NotAuthenticated.default_detail}
        )

    def test_post_workout_template_only_with_name(self):
        template_body = {
            'name': 'тренировка',
        }
        response = self.client.post(self.url, template_body)
        instance = WorkoutTemplate.objects.get(
            **template_body, created_by=self.user
        )
        serializer_data = WorkoutTemplateListCreateSerializer(instance).data

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer_data)

    def test_post_workout_template_with_all_fields(self):
        template_body = {
            'name': 'тренировка',
            'created_by': uuid.uuid4(),
            'break_between_approaches': 150,
        }
        response = self.client.post(self.url, template_body)
        template_body['created_by'] = self.user
        instance = WorkoutTemplate.objects.get(**template_body)
        serializer_data = WorkoutTemplateListCreateSerializer(instance).data

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer_data)

    def test_post_workout_template_with_already_exists_name(self):
        template_body = {
            'name': 'тест треня',
            'created_by': self.user,
            'break_between_approaches': 150,
        }
        WorkoutTemplate.objects.create(**template_body)
        response = self.client.post(self.url, template_body)

        error_response = {'non_field_errors': [ErrorDetail(
            string='Workout template with this name for this user already exists', code='unique')
        ]}

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, error_response)


class GETWorkoutTemplateViewTestCases(APITestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.url_name = 'manage_template'

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
        self.client.login(
            username=default_username,
            password=default_password
        )


class PUTWorkoutTemplateViewTestCases(APITestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.url_name = 'manage_template'

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
        self.client.login(
            username=default_username,
            password=default_password
        )


class PATCHWorkoutTemplateViewTestCases(APITestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.url_name = 'manage_template'

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
        self.client.login(
            username=default_username,
            password=default_password
        )


class DELETEWorkoutTemplateViewTestCases(APITestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.url_name = 'manage_template'

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
        self.client.login(
            username=default_username,
            password=default_password
        )


class LISTExerciseInWorkoutTemplateViewTestCases(APITestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.url = reverse_lazy('create_and_list_exercises_in_template')

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
        self.client.login(
            username=default_username,
            password=default_password
        )


class POSTExerciseInWorkoutTemplateViewTestCases(APITestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.url = reverse_lazy('create_and_list_exercises_in_template')

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
        self.client.login(
            username=default_username,
            password=default_password
        )


class GETExerciseInWorkoutTemplateViewTestCases(APITestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.url_name = 'manage_exercise_in_template'

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
        self.client.login(
            username=default_username,
            password=default_password
        )


class PUTExerciseInWorkoutTemplateViewTestCases(APITestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.url_name = 'manage_exercise_in_template'

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
        self.client.login(
            username=default_username,
            password=default_password
        )


class PATCHExerciseInWorkoutTemplateViewTestCases(APITestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.url_name = 'manage_exercise_in_template'

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
        self.client.login(
            username=default_username,
            password=default_password
        )


class DELETEExerciseInWorkoutTemplateViewTestCases(APITestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.url_name = 'manage_exercise_in_template'

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
        self.client.login(
            username=default_username,
            password=default_password
        )


class LISTExerciseApproachInWorkoutTemplateViewTestCases(APITestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.url = reverse_lazy('create_and_list_exercise_approach_in_template')


class POSTExerciseApproachInWorkoutTemplateViewTestCases(APITestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.url = reverse_lazy('create_and_list_exercise_approach_in_template')


class GETExerciseApproachInWorkoutTemplateViewTestCases(APITestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.url_name = 'manage_exercise_approach_in_template'

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
        self.client.login(
            username=default_username,
            password=default_password
        )


class PUTExerciseApproachInWorkoutTemplateViewTestCases(APITestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.url_name = 'manage_exercise_approach_in_template'

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
        self.client.login(
            username=default_username,
            password=default_password
        )


class PATCHExerciseApproachInWorkoutTemplateViewTestCases(APITestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.url_name = 'manage_exercise_approach_in_template'

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
        self.client.login(
            username=default_username,
            password=default_password
        )


class DELETEExerciseApproachInWorkoutTemplateViewTestCases(APITestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.url_name = 'manage_exercise_approach_in_template'

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
        self.client.login(
            username=default_username,
            password=default_password
        )
