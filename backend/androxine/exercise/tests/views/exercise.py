from django.urls import reverse_lazy
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.request import Request
from rest_framework.settings import api_settings
from rest_framework.test import APITestCase, DjangoRequestFactory
from rest_framework.exceptions import NotAuthenticated, PermissionDenied

from exercise.documents import ExerciseDocument
from exercise.services import get_exercise_elasticsearch_query
from exercise.models import ExerciseCategory, Exercise
from exercise.serializers import ExerciseListSerializer, ExerciseCreateSerializer

UserModel = get_user_model()


class ExerciseCreateViewTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.url = reverse_lazy('exercise_list_create')

    def setUp(self) -> None:
        self.username = 'user'
        self.password = '23fcf453DSdhej#_d'

        self.user = UserModel.objects.create_superuser(
            username=self.username,
            email='user@test.com',
            password=self.password,
        )
        self.nogi = ExerciseCategory.objects.create(name='ноги')
        self.client.login(
            username=self.username,
            password=self.password,
        )

    def test_create_exercise_by_non_auth_user(self):
        self.client.logout()
        request_data = {
            'name': 'присед',
            'category': self.nogi,
        }
        response = self.client.post(self.url, request_data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, {
            'detail': NotAuthenticated.default_detail
        })

    def test_create_exercise_by_common_auth_user(self):
        self.client.logout()
        UserModel.objects.create_user(
            username='common_user',
            email='common@test.com',
            password='23fcf453DSdhej#_d',
        )
        self.client.login(
            username='common_user',
            password='23fcf453DSdhej#_d',
        )
        request_data = {
            'name': 'присед',
            'category': self.nogi,
        }
        response = self.client.post(self.url, request_data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, {
            'detail': PermissionDenied.default_detail
        })

    def test_create_exercise_by_loggedin_admin_user(self):
        request_data = {
            'name': 'присед',
            'category': self.nogi.pk,
        }
        response = self.client.post(self.url, request_data)
        instance = Exercise.objects.get(**request_data)
        serializer_data = ExerciseCreateSerializer(instance).data

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer_data)

    def test_create_exercise_with_non_existing_category_id(self):
        request_data = {
            'name': 'присед',
            'category_id': 5,
        }
        response = self.client.post(self.url, request_data)
        serializer = ExerciseCreateSerializer(data=request_data)
        serializer.is_valid()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, serializer.errors)

    def test_create_exercise_with_already_existing_name_for_this_category(self):
        request_data = {
            'name': 'присед',
            'category': self.nogi.pk,
        }
        Exercise.objects.create(**{
            'name': 'присед',
            'category': self.nogi,
        })
        response = self.client.post(self.url, request_data)
        serializer = ExerciseCreateSerializer(data=request_data)
        serializer.is_valid()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, serializer.errors)
