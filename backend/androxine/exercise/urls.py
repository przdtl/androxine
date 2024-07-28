from django.urls import path

from exercise.views import ExerciseCategoryListView, ExerciseListView

urlpatterns = [
    path('', ExerciseListView.as_view(), name='exercise_list'),
    path('category/', ExerciseCategoryListView.as_view(),
         name='exercise_category_list'),
]
