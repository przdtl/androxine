from django.urls import path

from workout_template.views import (
    WorkoutTemplateRetrieveUpdateView,
    WorkoutTemplateCreateListView,
    ExerciseInWorkoutTemplateCreateListView,
    ExerciseInWorkoutTemplateRetrieveUpdateView,
    ExerciseApproachInWorkoutTemplateCreateListView,
    ExerciseApproachInWorkoutTemplateRetrieveUpdateView,
)


urlpatterns = [
    path(
        '',
        WorkoutTemplateCreateListView.as_view(),
        name='create_and_list_templates'
    ),
    path(
        '<uuid:pk>/',
        WorkoutTemplateRetrieveUpdateView.as_view(),
        name='manage_template'
    ),
    path(
        'exercise/',
        ExerciseInWorkoutTemplateCreateListView.as_view(),
        name='create_and_list_exercises_in_template'
    ),
    path(
        'exercise/<uuid:pk>/',
        ExerciseInWorkoutTemplateRetrieveUpdateView.as_view(),
        name='manage_exercise_in_template'
    ),
    path(
        'approach/',
        ExerciseApproachInWorkoutTemplateCreateListView.as_view(),
        name='add_exercise_approach_in_template'
    ),
    path(
        'approach/<uuid:pk>/',
        ExerciseApproachInWorkoutTemplateRetrieveUpdateView.as_view(),
        name='manage_exercise_approach_in_template'
    )
]
