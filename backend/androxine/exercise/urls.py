from django.urls import path

from exercise.views import ExerciseCategoryListView, ExerciseListView

urlpatterns = [
    path('exercise/', ExerciseListView.as_view(), name='exercise_list'),
    path('exercise_category/', ExerciseCategoryListView.as_view(),
         name='exercise_category_list'),
]
