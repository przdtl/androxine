from rest_framework.generics import (
    ListAPIView, RetrieveUpdateAPIView, ListCreateAPIView
)
from config.utils import UpdateRequestManager

from exercise.models import ExerciseCategory, UserExerciseSettings
from exercise.documents import ExerciseDocument
from exercise.serializers import (
    ExerciseCategorySerializer, ExerciseSerializer, ReadUserExerciseSettingsSerializer, WriteUserExerciseSettingsSerializer
)
from exercise.services import get_exercise_elasticsearch_query

from config.utils import CustomGetObjectMixin


class ExerciseCategoryListView(ListAPIView):
    queryset = ExerciseCategory.objects.all()
    serializer_class = ExerciseCategorySerializer


class ExerciseListView(ListAPIView):
    serializer_class = ExerciseSerializer

    def get_queryset(self):
        category = self.request.query_params.get('category')
        name = self.request.query_params.get('name')

        search = ExerciseDocument.search().query(
            get_exercise_elasticsearch_query(name, category)
        )
        response = search.execute()

        return response


class UserExerciseSettingsRetrieveUpdateView(CustomGetObjectMixin, RetrieveUpdateAPIView):
    serializer_class = ReadUserExerciseSettingsSerializer
    queryset = UserExerciseSettings.objects.all()
    lookup_fields = {'exercise__slug': 'slug'}
    shadow_user_lookup_field = 'user'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class UserExerciseSettingsListCreateView(ListCreateAPIView):
    serializer_class = WriteUserExerciseSettingsSerializer
    queryset = UserExerciseSettings.objects.all()

    def get_queryset(self):
        user_id = self.request.user.pk
        return UserExerciseSettings.objects.filter(
            user_id=user_id
        )

    def post(self, request, *args, **kwargs):
        with UpdateRequestManager(request.data):
            request.data.update({'user': request.user.pk})

        return super().post(request, *args, **kwargs)
