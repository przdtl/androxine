from rest_framework.generics import ListAPIView

from exercise.models import Exercise, ExerciseCategory
from exercise.serializers import ExerciseCategorySerializer, ExerciseSerializer


class ExerciseCategoryListView(ListAPIView):
    queryset = ExerciseCategory.objects.all()
    serializer_class = ExerciseCategorySerializer


class ExerciseListView(ListAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
