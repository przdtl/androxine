from django.urls import path

from exercise.views import (
    ExerciseCategoryListView, ExerciseListView, UserExerciseSettingsRetrieveUpdateDestroyView, UserExerciseSettingsListCreateView
)

urlpatterns = [
    path('', ExerciseListView.as_view(), name='exercise_list'),
    path('category/', ExerciseCategoryListView.as_view(),
         name='exercise_category_list'),
]

exercise_settings_urlpatterns = [
    path('settings/', UserExerciseSettingsListCreateView.as_view(),
         name='list_create_exercise_settings'),
    path('settings/<slug:slug>/', UserExerciseSettingsRetrieveUpdateDestroyView.as_view(),
         name='manage_exercise_settings'),
]

urlpatterns += exercise_settings_urlpatterns
