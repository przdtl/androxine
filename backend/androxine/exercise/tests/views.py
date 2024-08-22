from django.urls import reverse_lazy
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.request import Request
from rest_framework.settings import api_settings
from rest_framework.test import APITestCase, DjangoRequestFactory
from rest_framework.exceptions import NotAuthenticated, ErrorDetail

from exercise.documents import ExerciseDocument
from exercise.views import UserExerciseSettingsListCreateView
from exercise.services import get_exercise_elasticsearch_query
from exercise.models import ExerciseCategory, Exercise, UserExerciseSettings
from exercise.serializers import (
    ExerciseCategorySerializer, ExerciseListSerializer,
    UserExerciseSettingsManageSerializer, UserExerciseSettingsListCreateSerializer
)

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


class GETUserExerciseSettings(APITestCase):
    def setUp(self) -> None:
        super().setUp()
        self.username = 'user'
        self.password = 'asdSsd4223_ssas42?'
        self.user = UserModel.objects.create_user(
            username=self.username,
            email='user.user@gmail.com',
            password=self.password,
        )
        self.nogi = ExerciseCategory.objects.create(name='ноги')
        self.prised = Exercise.objects.create(
            name='присед', category_id=self.nogi.pk)
        self.assertTrue(self.client.login(
            username=self.username, password=self.password)
        )

    def test_get_exercise_settings_by_non_logging_user(self):
        self.client.logout()
        url = reverse_lazy('manage_exercise_settings', args=['prised'])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data, {'detail': NotAuthenticated.default_detail})

    def test_get_exercise_settings(self):
        settings = UserExerciseSettings.objects.create(
            user_id=self.user.pk,
            exercise_id=self.prised.pk,
            one_time_maximum=101,
        )
        url = reverse_lazy('manage_exercise_settings', args=['prised'])
        response = self.client.get(url)
        serializer_data = UserExerciseSettingsManageSerializer(settings).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer_data)

    def test_get_exercise_settings_about_not_existed_exercise(self):
        url = reverse_lazy('manage_exercise_settings', args=['zhim'])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, user_exerxise_settings_error_response)

    def test_get_not_existed_exercise_settings(self):
        url = reverse_lazy('manage_exercise_settings', args=['prised'])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, user_exerxise_settings_error_response)


class PUTUserExerciseSettings(APITestCase):
    def setUp(self) -> None:
        self.user = UserModel.objects.create_user(
            username='user',
            email='user.user@gmail.com',
            password='asdSsd4223_ssas42?',
        )
        self.nogi = ExerciseCategory.objects.create(name='ноги')
        self.prised = Exercise.objects.create(
            name='присед', category_id=self.nogi.pk)
        self.prised_settings = UserExerciseSettings.objects.create(
            user_id=self.user.pk,
            exercise_id=self.prised.pk,
            one_time_maximum=101.0,
        )
        self.client.login(
            username='user',
            password='asdSsd4223_ssas42?',
        )

    def test_put_exercise_settings_by_non_logging_user(self):
        self.client.logout()
        url = reverse_lazy('manage_exercise_settings', args=['prised'])
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data, {'detail': NotAuthenticated.default_detail})

    def test_put_not_existed_exercise_settings(self):
        settings_data = {
            'one_time_maximum': 101.0,
        }
        url = reverse_lazy('manage_exercise_settings', args=['zhim'])
        response = self.client.put(url, settings_data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, user_exerxise_settings_error_response)

    def test_put_all_exercise_settings(self):
        settings_data = {
            'one_time_maximum': 101.0,
        }
        url = reverse_lazy('manage_exercise_settings', args=['prised'])
        response = self.client.put(url, settings_data)
        serializer_data = UserExerciseSettingsManageSerializer(
            self.prised_settings).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer_data)

    def test_put_partial_exercise_settings(self):
        settings_data = {}
        url = reverse_lazy('manage_exercise_settings', args=['prised'])
        response = self.client.put(url, settings_data)

        error = {'one_time_maximum': [ErrorDetail(
            string='Обязательное поле.', code='required')]}

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, error)


class PATCHUserExerciseSettings(APITestCase):
    def setUp(self) -> None:
        self.user = UserModel.objects.create_user(
            username='user',
            email='user.user@gmail.com',
            password='asdSsd4223_ssas42?',
        )
        self.nogi = ExerciseCategory.objects.create(name='ноги')
        self.prised = Exercise.objects.create(
            name='присед', category_id=self.nogi.pk)
        self.prised_settings = UserExerciseSettings.objects.create(
            user_id=self.user.pk,
            exercise_id=self.prised.pk,
            one_time_maximum=101.0,
        )
        self.client.login(
            username='user',
            password='asdSsd4223_ssas42?',
        )

    def test_put_exercise_settings_by_non_logging_user(self):
        self.client.logout()
        url = reverse_lazy('manage_exercise_settings', args=['prised'])
        response = self.client.patch(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data, {'detail': NotAuthenticated.default_detail})

    def test_put_not_existed_exercise_settings(self):
        settings_data = {
            'one_time_maximum': 101.0,
        }
        url = reverse_lazy('manage_exercise_settings', args=['zhim'])
        response = self.client.patch(url, settings_data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, user_exerxise_settings_error_response)

    def test_put_all_exercise_settings(self):
        settings_data = {
            'one_time_maximum': 101.0,
        }
        url = reverse_lazy('manage_exercise_settings', args=['prised'])
        response = self.client.patch(url, settings_data)
        serializer_data = UserExerciseSettingsManageSerializer(
            self.prised_settings).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer_data)

    def test_put_partial_exercise_settings(self):
        settings_data = {}
        url = reverse_lazy('manage_exercise_settings', args=['prised'])
        response = self.client.patch(url, settings_data)
        serializer_data = UserExerciseSettingsManageSerializer(
            self.prised_settings).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer_data)


class DELETEUserExerciseSettings(APITestCase):
    def setUp(self) -> None:
        self.user = UserModel.objects.create_user(
            username='user',
            email='user.user@gmail.com',
            password='asdSsd4223_ssas42?',
        )
        self.nogi = ExerciseCategory.objects.create(name='ноги')
        self.prised = Exercise.objects.create(
            name='присед', category_id=self.nogi.pk)
        self.prised_settings = UserExerciseSettings.objects.create(
            user_id=self.user.pk,
            exercise_id=self.prised.pk,
            one_time_maximum=101.0,
        )
        self.client.login(
            username='user',
            password='asdSsd4223_ssas42?',
        )

    def test_delete_exercise_settings_by_non_logging_user(self):
        self.client.logout()
        url = reverse_lazy('manage_exercise_settings', args=['prised'])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data, {'detail': NotAuthenticated.default_detail})

    def test_delete_not_existed_exercise_settings(self):
        url = reverse_lazy('manage_exercise_settings', args=['zhim'])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, user_exerxise_settings_error_response)

    def test_delete_exercise_settings(self):
        url = reverse_lazy('manage_exercise_settings', args=['prised'])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, None)


class POSTUserExerciseSettings(APITestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.url = reverse_lazy('list_create_exercise_settings')
        cls.request_factory_class = DjangoRequestFactory

    def setUp(self) -> None:
        self.user = UserModel.objects.create_user(
            username='user',
            email='user.user@gmail.com',
            password='asdSsd4223_ssas42?',
        )
        self.nogi = ExerciseCategory.objects.create(name='ноги')
        self.prised = Exercise.objects.create(
            name='присед', category_id=self.nogi.pk)
        self.client.login(
            username='user',
            password='asdSsd4223_ssas42?',
        )

    def test_post_exercise_settings_by_non_logging_user(self):
        self.client.logout()
        factory = self.request_factory_class()
        view = UserExerciseSettingsListCreateView.as_view()
        request = factory.post(self.url)
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data, {'detail': NotAuthenticated.default_detail})

    def test_post_exercise_settings(self):
        settings_data = {
            'exercise': self.prised.id,
            'one_time_maximum': 101.0,
        }
        response = self.client.post(self.url, settings_data)
        settings = UserExerciseSettings.objects.get(
            user_id=self.user.pk,
            exercise_id=self.prised.id
        )
        serializer_data = UserExerciseSettingsListCreateSerializer(
            instance=settings
        ).data

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer_data)

    def test_post_exercise_settings_with_non_existing_exercise(self):
        settings_data = {
            'exercise': 'zhim',
            'one_time_maximum': 101,
        }
        serializer_settings_data = settings_data.copy()
        serializer_settings_data['user'] = self.user.pk
        response = self.client.post(self.url, settings_data)
        serializer = UserExerciseSettingsListCreateSerializer(
            data=serializer_settings_data)
        serializer.is_valid()
        serializer_errors = serializer.errors

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, serializer_errors)

    def test_post_exercise_settings_with_already_existing_instance(self):
        UserExerciseSettings.objects.create(
            user_id=self.user.pk,
            exercise_id=self.prised.pk,
            one_time_maximum=144
        )
        settings_data = {
            'exercise': self.prised.slug,
            'one_time_maximum': 101,
        }
        serializer_settings_data = settings_data.copy()
        serializer_settings_data['user'] = self.user.pk
        response = self.client.post(self.url, settings_data)
        serializer = UserExerciseSettingsListCreateSerializer(
            data=serializer_settings_data)
        serializer.is_valid()
        serializer_errors = serializer.errors

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, serializer_errors)


class ListUserExerciseSettings(APITestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.url = reverse_lazy('list_create_exercise_settings')
        cls.pagination_class = api_settings.DEFAULT_PAGINATION_CLASS

    def setUp(self) -> None:
        self.user = UserModel.objects.create_user(
            username='user',
            email='user.user@gmail.com',
            password='asdSsd4223_ssas42?',
        )
        self.nogi = ExerciseCategory.objects.create(name='ноги')
        self.prised = Exercise.objects.create(
            name='присед', category_id=self.nogi.pk)
        self.client.login(
            username='user',
            password='asdSsd4223_ssas42?',
        )

    def test_list_exercise_settings_by_non_logging_user(self):
        self.client.logout()
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data, {'detail': NotAuthenticated.default_detail})

    def test_list_empty_exercise_settings(self):
        response = self.client.get(self.url)
        UserExerciseSettings.objects.all().delete()
        queryset = UserExerciseSettings.objects.none()

        factory = DjangoRequestFactory()
        request = Request(factory.get(self.url))

        pagination_obj = self.pagination_class()
        settings_data = pagination_obj.paginate_queryset(queryset, request)
        pagination_response = pagination_obj.get_paginated_response(
            UserExerciseSettingsListCreateSerializer(
                settings_data, many=True).data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, pagination_response.data)

    def test_list_not_empty_exercise_settings(self):
        Exercise.objects.bulk_create([
            Exercise(category=self.nogi, name='жим'),
            Exercise(category=self.nogi, name='разгибание ног')
        ])
        response = self.client.get(self.url)
        queryset = UserExerciseSettings.objects.all()

        factory = DjangoRequestFactory()
        request = Request(factory.get(self.url))

        pagination_obj = self.pagination_class()
        settings_data = pagination_obj.paginate_queryset(queryset, request)
        pagination_response = pagination_obj.get_paginated_response(
            UserExerciseSettingsListCreateSerializer(
                settings_data, many=True).data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, pagination_response.data)
