from django.urls import path, include

from workout_template.views import (
    WorkoutTemplateCreateListView,
    ExerciseInWorkoutTemplateReorderView,
    ExerciseInWorkoutTemplateCreateListView,
    WorkoutTemplateRetrieveUpdateDestroyView,
    ExerciseApproachInWorkoutTemplateReorderView,
    ExerciseApproachInWorkoutTemplateCreateListView,
    ExerciseInWorkoutTemplateRetrieveUpdateDestroyView,
    ExerciseApproachInWorkoutTemplateRetrieveUpdateDestroyView,
)

exercise_urlpatterns = [
    path(
        '',
        ExerciseInWorkoutTemplateCreateListView.as_view(),
        name='create_and_list_exercises_in_template'
    ),
    path(
        '<uuid:pk>/',
        ExerciseInWorkoutTemplateRetrieveUpdateDestroyView.as_view(),
        name='manage_exercise_in_template'
    ),
    path('reorder/', ExerciseInWorkoutTemplateReorderView.as_view(),
         name='reorder_exercises'),
]

approach_urlpatterns = [
    path(
        '',
        ExerciseApproachInWorkoutTemplateCreateListView.as_view(),
        name='create_and_list_exercise_approach_in_template'
    ),
    path(
        '<uuid:pk>/',
        ExerciseApproachInWorkoutTemplateRetrieveUpdateDestroyView.as_view(),
        name='manage_exercise_approach_in_template'
    ),
    path('reorder/', ExerciseApproachInWorkoutTemplateReorderView.as_view(),
         name='reorder_approaches'),
]

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
    path('exercise/', include(exercise_urlpatterns)),
    path('approach/', include(approach_urlpatterns)),

]
