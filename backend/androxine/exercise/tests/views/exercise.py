from django.urls import reverse_lazy
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.request import Request
from rest_framework.settings import api_settings
from rest_framework.test import APITestCase, DjangoRequestFactory
from rest_framework.exceptions import NotAuthenticated

from exercise.models import ExerciseCategory
from exercise.serializers import ExerciseCategorySerializer

UserModel = get_user_model()


class ExerciseCategoryListViewTest(APITestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.url = reverse_lazy('exercise_category_list')
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

    def test_category_list_by_not_logged_in_user(self):
        self.client.logout()

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data, {'detail': NotAuthenticated.default_detail})

    def test_non_empty_category_list_by_logged_in_user(self):
        categories = ['бицепс', 'ноги', 'плечи',
                      'трицепс', 'пресс', 'предплечье'
                      ]
        ExerciseCategory.objects.bulk_create(
            ExerciseCategory(name=category) for category in categories)
        response = self.client.get(self.url)
        queryset = ExerciseCategory.objects.all()

        factory = DjangoRequestFactory()
        request = Request(factory.get(self.url))

        pagination_obj = self.pagination_class()
        categories_data = pagination_obj.paginate_queryset(queryset, request)
        pagination_response = pagination_obj.get_paginated_response(
            ExerciseCategorySerializer(categories_data, many=True).data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, pagination_response.data)
