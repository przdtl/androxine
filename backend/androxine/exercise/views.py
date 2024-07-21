from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView

from elasticsearch_dsl import Q

from exercise.models import ExerciseCategory
from exercise.documents import ExerciseDocument
from exercise.serializers import ExerciseCategorySerializer, ExerciseSerializer


class ExerciseCategoryListView(ListAPIView):
    queryset = ExerciseCategory.objects.all()
    serializer_class = ExerciseCategorySerializer

    def get_queryset(self):
        return super().get_queryset()


class ExerciseListView(ListAPIView):
    serializer_class = ExerciseSerializer

    def get_elasticsearch_query(self):
        category = self.request.query_params.get('category')
        name = self.request.query_params.get('name')

        matches = []
        if category:
            matches.append({"match": {"category": category}})
        if name:
            matches.append({"match": {"name": name}})

        if matches:
            elasticsearch_query = Q({
                "bool": {
                    "should": matches
                }
            })
        else:
            elasticsearch_query = Q({
                "match_all": {},
            })

        return elasticsearch_query

    def get_queryset(self):
        search = ExerciseDocument.search().query(self.get_elasticsearch_query())
        response = search.execute()

        return response
