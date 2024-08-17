from django.urls import path

from workout_template.views import (
    WorkoutTemplateCreateListView,
    ExerciseInWorkoutTemplateCreateListView,
    WorkoutTemplateRetrieveUpdateDestroyView,
    ExerciseApproachInWorkoutTemplateCreateListView,
    ExerciseInWorkoutTemplateRetrieveUpdateDestroyView,
    ExerciseApproachInWorkoutTemplateRetrieveUpdateDestroyView,
)


urlpatterns = [
    path(
        '',
        WorkoutTemplateCreateListView.as_view(),
        name='create_and_list_templates'
    ),
    path(
        '<uuid:pk>/',
        WorkoutTemplateRetrieveUpdateDestroyView.as_view(),
        name='manage_template'
    ),
    path(
        'exercise/',
        ExerciseInWorkoutTemplateCreateListView.as_view(),
        name='create_and_list_exercises_in_template'
    ),
    path(
        'exercise/<uuid:pk>/',
        ExerciseInWorkoutTemplateRetrieveUpdateDestroyView.as_view(),
        name='manage_exercise_in_template'
    ),
    path(
        'approach/',
        ExerciseApproachInWorkoutTemplateCreateListView.as_view(),
        name='create_and_list_exercise_approach_in_template'
    ),
    path(
        'approach/<uuid:pk>/',
        ExerciseApproachInWorkoutTemplateRetrieveUpdateDestroyView.as_view(),
        name='manage_exercise_approach_in_template'
    )
]
