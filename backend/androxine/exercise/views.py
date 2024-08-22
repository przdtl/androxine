from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import (
    ListAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView,
)
from drf_yasg.utils import swagger_auto_schema

from config.utils import UpdateRequestManager
from config.permissions import IsAdminOrAuthReadOnly

from exercise.models import Exercise, ExerciseCategory, UserExerciseSettings
from exercise.documents import ExerciseDocument
from exercise.serializers import (
    ExerciseListSerializer,
    ExericseManageSerializer,
    ExerciseCreateSerializer,
    ExerciseCategorySerializer,
    ExerciseListSwaggerSerializer,
    UserExerciseSettingsManageSerializer,
    UserExerciseSettingsListCreateSerializer,
    UserExerciseSettingsListSwaggerSerializer,
    UserExerciseSettingsManageSwaggerSerializer,
)
from exercise.services import get_exercise_elasticsearch_query

from config.utils import CustomGetObjectMixin


class ExerciseCategoryListView(ListAPIView):
    queryset = ExerciseCategory.objects.all()
    serializer_class = ExerciseCategorySerializer


class ExerciseListView(ListCreateAPIView):
    list_serializer_class = ExerciseListSerializer
    create_serializer_class = ExerciseCreateSerializer
    permission_classes = [IsAdminOrAuthReadOnly]

    def get_queryset(self):
        input_serializer = ExerciseListSwaggerSerializer(
            data=self.request.query_params
        )
        input_serializer.is_valid(raise_exception=True)

        category = input_serializer.data.get('category')
        name = input_serializer.data.get('name')

        search = ExerciseDocument.search().query(
            get_exercise_elasticsearch_query(name, category)
        )
        response = search.execute()

        return response

    @swagger_auto_schema(
        query_serializer=ExerciseListSwaggerSerializer,
        responses={200: ExerciseListSwaggerSerializer},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=ExerciseCreateSerializer,
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.list_serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.list_serializer_class(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.create_serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ExerciseRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = ExericseManageSerializer
    queryset = Exercise.objects.all()
    permission_classes = [IsAdminOrAuthReadOnly]
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'


class UserExerciseSettingsListCreateView(ListCreateAPIView):
    serializer_class = UserExerciseSettingsListCreateSerializer

    def get_queryset(self):
        return UserExerciseSettings.objects.filter(
            user_id=self.request.user.pk
        )

    @swagger_auto_schema(
        tags=['exercise_settings'],
        request_body=UserExerciseSettingsListSwaggerSerializer,
        responses={201: UserExerciseSettingsListCreateSerializer},
    )
    def post(self, request, *args, **kwargs):
        with UpdateRequestManager(request.data):
            request.data.update({'user': request.user.pk})

        return super().post(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['exercise_settings']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class UserExerciseSettingsRetrieveUpdateDestroyView(CustomGetObjectMixin, RetrieveUpdateDestroyAPIView):
    serializer_class = UserExerciseSettingsManageSerializer
    queryset = UserExerciseSettings.objects.all()
    lookup_fields = {'exercise__slug': 'slug'}
    shadow_user_lookup_field = 'user'

    @swagger_auto_schema(tags=['exercise_settings'])
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['exercise_settings'],
        request_body=UserExerciseSettingsManageSwaggerSerializer,
        responses={200: UserExerciseSettingsManageSerializer},
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['exercise_settings'],
        request_body=UserExerciseSettingsManageSwaggerSerializer,
        responses={200: UserExerciseSettingsManageSerializer},
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['exercise_settings'])
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
