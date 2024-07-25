from rest_framework.generics import ListAPIView

from exercise.models import ExerciseCategory
from exercise.documents import ExerciseDocument
from exercise.serializers import ExerciseCategorySerializer, ExerciseSerializer
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
