from django.urls import reverse_lazy
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.request import Request
from rest_framework.settings import api_settings
from rest_framework.test import APITestCase, DjangoRequestFactory
from rest_framework.exceptions import NotAuthenticated, ErrorDetail

from exercise.documents import ExerciseDocument
from exercise.services import get_exercise_elasticsearch_query
from exercise.models import ExerciseCategory, Exercise
from exercise.serializers import ExerciseListSerializer

UserModel = get_user_model()


class EmptyExerciseListViewTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.url = reverse_lazy('exercise_list')
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

    def test_exercise_list_by_not_logged_in_user(self):
        self.client.logout()

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data, {'detail': NotAuthenticated.default_detail})

    def test_exercise_list_without_query_params(self):
        response = self.client.get(self.url)
        queryset = ExerciseDocument.search().query(
            get_exercise_elasticsearch_query()
        ).execute()

        factory = DjangoRequestFactory()
        request = Request(factory.get(self.url))

        pagination_obj = self.pagination_class()
        categories_data = pagination_obj.paginate_queryset(queryset, request)
        pagination_response = pagination_obj.get_paginated_response(
            ExerciseListSerializer(categories_data, many=True).data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, pagination_response.data)

    def test_exercise_list_with_name(self):
        name = 'жим'
        response = self.client.get(self.url, {'name': name})
        queryset = ExerciseDocument.search().query(
            get_exercise_elasticsearch_query(name=name)
        ).execute()

        factory = DjangoRequestFactory()
        request = Request(factory.get(self.url), {'name': name})

        pagination_obj = self.pagination_class()
        categories_data = pagination_obj.paginate_queryset(queryset, request)
        pagination_response = pagination_obj.get_paginated_response(
            ExerciseListSerializer(categories_data, many=True).data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, pagination_response.data)

    def test_exercise_list_with_category(self):
        category = 'ноги'
        response = self.client.get(self.url, {'category': category})
        queryset = ExerciseDocument.search().query(
            get_exercise_elasticsearch_query(category=category)
        ).execute()

        factory = DjangoRequestFactory()
        request = Request(factory.get(self.url), {'category': category})

        pagination_obj = self.pagination_class()
        categories_data = pagination_obj.paginate_queryset(queryset, request)
        pagination_response = pagination_obj.get_paginated_response(
            ExerciseListSerializer(categories_data, many=True).data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, pagination_response.data)


class NonEmptyExerciseListViewTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.url = reverse_lazy('exercise_list')
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

        self.nogi = ExerciseCategory.objects.create(name='ноги')
        self.grud = ExerciseCategory.objects.create(name='грудь')
        nogi_exercises = ['присед', 'жим']
        grud_exercises = ['разводка', 'бабочка']
        Exercise.objects.bulk_create(
            [Exercise(name=name, category_id=self.nogi.pk) for name in nogi_exercises])
        Exercise.objects.bulk_create(
            [Exercise(name=name, category_id=self.grud.pk) for name in grud_exercises])

    def test_exercise_list_without_query_params(self):
        response = self.client.get(self.url)
        queryset = ExerciseDocument.search().query(
            get_exercise_elasticsearch_query()
        ).execute()

        factory = DjangoRequestFactory()
        request = Request(factory.get(self.url))

        pagination_obj = self.pagination_class()
        categories_data = pagination_obj.paginate_queryset(queryset, request)
        pagination_response = pagination_obj.get_paginated_response(
            ExerciseListSerializer(categories_data, many=True).data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, pagination_response.data)

    def test_exercise_list_with_name(self):
        name = 'жим'
        response = self.client.get(self.url, {'name': name})
        queryset = queryset = ExerciseDocument.search().query(
            get_exercise_elasticsearch_query(name=name)
        ).execute()

        factory = DjangoRequestFactory()
        request = Request(factory.get(self.url), {'name': name})

        pagination_obj = self.pagination_class()
        categories_data = pagination_obj.paginate_queryset(queryset, request)
        pagination_response = pagination_obj.get_paginated_response(
            ExerciseListSerializer(categories_data, many=True).data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, pagination_response.data)

    def test_exercise_list_with_category(self):
        category = 'ноги'
        response = self.client.get(self.url, {'category': category})
        queryset = ExerciseDocument.search().query(
            get_exercise_elasticsearch_query(category=category)
        ).execute()

        factory = DjangoRequestFactory()
        request = Request(factory.get(self.url), {'category': category})

        pagination_obj = self.pagination_class()
        categories_data = pagination_obj.paginate_queryset(queryset, request)
        pagination_response = pagination_obj.get_paginated_response(
            ExerciseListSerializer(categories_data, many=True).data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, pagination_response.data)


user_exerxise_settings_error_response = {'detail': ErrorDetail(
    string='No UserExerciseSettings matches the given query.', code='not_found')}
