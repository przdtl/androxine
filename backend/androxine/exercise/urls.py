from django.urls import path, include

from exercise.views import (
    ExerciseListCreateView,
    ExerciseCategoryListCreateView,
    ExerciseRetrieveUpdateDestroyView,
    UserExerciseSettingsListCreateView,
    ExerciseCategoryRetrieveUpdateDestroyView,
    UserExerciseSettingsRetrieveUpdateDestroyView,
)

exercise_urlpatterns = [
    path('', ExerciseListCreateView.as_view(), name='exercise_list_create'),
    path('<slug:slug>/', ExerciseRetrieveUpdateDestroyView.as_view(),
         name='manage_exercise'),
]

exercise_category_urlpatterns = [
    path('', ExerciseCategoryListCreateView.as_view(),
         name='exercise_category_list_create'),
    path('<slug:slug>/', ExerciseCategoryRetrieveUpdateDestroyView.as_view(),
         name='manage_exercise_category')
]

exercise_settings_urlpatterns = [
    path('', UserExerciseSettingsListCreateView.as_view(),
         name='list_create_exercise_settings'),
    path('<slug:slug>/', UserExerciseSettingsRetrieveUpdateDestroyView.as_view(),
         name='manage_exercise_settings'),
]

urlpatterns = [
    path('category/', include(exercise_category_urlpatterns)),
    path('settings/', include(exercise_settings_urlpatterns)),
    path('', include(exercise_urlpatterns)),
]
