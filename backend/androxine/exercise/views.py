from rest_framework.generics import (
    ListAPIView, RetrieveUpdateAPIView, CreateAPIView, get_object_or_404
)

from exercise.models import ExerciseCategory, UserExerciseSettings
from exercise.documents import ExerciseDocument
from exercise.serializers import (
    ExerciseCategorySerializer, ExerciseSerializer, ReadUserExerciseSettingsSerializer, WriteUserExerciseSettingsSerializer
)
from exercise.services import get_exercise_elasticsearch_query


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


class UserExerciseSettingsRetrieveUpdateView(RetrieveUpdateAPIView):
    serializer_class = ReadUserExerciseSettingsSerializer
    queryset = UserExerciseSettings.objects.all()
    lookup_field = 'exercise__slug'
    lookup_url_kwarg = 'slug'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {
            self.lookup_field: self.kwargs[lookup_url_kwarg],
            'user': self.request.user.pk,
        }
        obj = get_object_or_404(queryset, **filter_kwargs)

        self.check_object_permissions(self.request, obj)

        return obj


class UserExerciseSettingsCreateView(CreateAPIView):
    serializer_class = WriteUserExerciseSettingsSerializer
    queryset = UserExerciseSettings.objects.all()

    def post(self, request, *args, **kwargs):
        request.data._mutable = True
        request.data['user'] = request.user.pk
        request.data._mutable = False
        return super().post(request, *args, **kwargs)
