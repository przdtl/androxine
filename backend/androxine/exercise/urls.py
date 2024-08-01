from django.urls import path

from exercise.views import (
    ExerciseCategoryListView, ExerciseListView, UserExerciseSettingsRetrieveUpdateView, UserExerciseSettingsCreateView
)

urlpatterns = [
    path('', ExerciseListView.as_view(), name='exercise_list'),
    path('category/', ExerciseCategoryListView.as_view(),
         name='exercise_category_list'),
]

exercise_settings_urlpatterns = [
    path('settings/', UserExerciseSettingsCreateView.as_view(),
         name='create_exercise_settings'),
    path('settings/<slug:slug>/', UserExerciseSettingsRetrieveUpdateView.as_view(),
         name='manage_exercise_settings'),
]

urlpatterns += exercise_settings_urlpatterns
