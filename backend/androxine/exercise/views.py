from rest_framework.generics import (
    ListAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView,
)
from drf_yasg.utils import swagger_auto_schema

from config.utils import UpdateRequestManager

from exercise.models import ExerciseCategory, UserExerciseSettings
from exercise.documents import ExerciseDocument
from exercise.serializers import (
    ExerciseSerializer,
    ExerciseCategorySerializer,
    ExerciseListSwaggerSerializer,
    ReadUserExerciseSettingsSerializer,
    WriteUserExerciseSettingsSerializer
)
from exercise.services import get_exercise_elasticsearch_query

from config.utils import CustomGetObjectMixin


class ExerciseCategoryListView(ListAPIView):
    queryset = ExerciseCategory.objects.all()
    serializer_class = ExerciseCategorySerializer


class ExerciseListView(ListAPIView):
    serializer_class = ExerciseSerializer

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
        query_serializer=ExerciseListSwaggerSerializer
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class UserExerciseSettingsRetrieveUpdateDestroyView(CustomGetObjectMixin, RetrieveUpdateDestroyAPIView):
    serializer_class = ReadUserExerciseSettingsSerializer
    queryset = UserExerciseSettings.objects.all()
    lookup_fields = {'exercise__slug': 'slug'}
    shadow_user_lookup_field = 'user'

    @swagger_auto_schema(tags=['exercise_settings'])
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=['exercise_settings'])
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['exercise_settings'])
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['exercise_settings'])
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class UserExerciseSettingsListCreateView(ListCreateAPIView):
    serializer_class = WriteUserExerciseSettingsSerializer
    queryset = UserExerciseSettings.objects.all()

    def get_queryset(self):
        user_id = self.request.user.pk
        return UserExerciseSettings.objects.filter(
            user_id=user_id
        )

    @swagger_auto_schema(tags=['exercise_settings'])
    def post(self, request, *args, **kwargs):
        with UpdateRequestManager(request.data):
            request.data.update({'user': request.user.pk})

        return super().post(request, *args, **kwargs)

    @swagger_auto_schema(tags=['exercise_settings'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
