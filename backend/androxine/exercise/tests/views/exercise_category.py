from django.urls import reverse_lazy
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.request import Request
from rest_framework.settings import api_settings
from rest_framework.test import APITestCase, DjangoRequestFactory

from exercise.models import ExerciseCategory
from exercise.serializers import ExerciseCategorySerializer

UserModel = get_user_model()


class ExerciseCategoryListViewTestCase(APITestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.url = reverse_lazy('exercise_category_list_create')
        cls.pagination_class = api_settings.DEFAULT_PAGINATION_CLASS

    def setUp(self) -> None:
        self.username = 'user'
        self.password = '23fcf453DSdhej#_d'

        UserModel.objects.create_user(
            username=self.username,
            email='user@test.com',
            password=self.password,
        )

        self.client.login(
            username=self.username,
            password=self.password,
        )

    def test_empty_category_list_by_logged_in_user(self):
        response = self.client.get(self.url)
        queryset = ExerciseCategory.objects.none()

        factory = DjangoRequestFactory()
        request = Request(factory.get(self.url))

        pagination_obj = self.pagination_class()
        categories_data = pagination_obj.paginate_queryset(queryset, request)
        pagination_response = pagination_obj.get_paginated_response(
            ExerciseCategorySerializer(categories_data, many=True).data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, pagination_response.data)


class ExerciseCategoryCreateViewTestCase(APITestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.url = reverse_lazy('exercise_category_list_create')

    def setUp(self) -> None:
        self.username = 'user'
        self.password = '23fcf453DSdhej#_d'

        self.user = UserModel.objects.create_superuser(
            username=self.username,
            email='user@test.com',
            password=self.password,
        )
        self.client.login(
            username=self.username,
            password=self.password,
        )
