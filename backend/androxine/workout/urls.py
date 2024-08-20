from django.urls import path, include

from workout.views import (
    WorkoutListView,
    ApproachListCreateView,
    WorkoutCreateView,
    FinishWorkoutView,
    WorkoutRetrieveView,
    GetUnfinishedWorkoutView,
    ExerciseInWorkoutListView,
    WorkoutCreateByTemplateView,
    ApproachByTemplateCreateView,
    ExerciseInWorkoutRetrieveView,
    ApproachRetrieveUpdateDestroyView,
)

create_workout_urlpatterns = [
    path('', WorkoutCreateView.as_view(), name='create_workout'),
    path('by_template/', WorkoutCreateByTemplateView.as_view(),
         name='create_workout_by_template'),
]

approach_urlpatterns = [
    path('', ApproachListCreateView.as_view(), name='add_approach'),
    path('by_template/', ApproachByTemplateCreateView.as_view(),
         name='add_approach_by_template'),
    path('<uuid:pk>/', ApproachRetrieveUpdateDestroyView.as_view(),
         name='manage_approach'),
]

exercise_urlpatterns = [
    path('', ExerciseInWorkoutListView.as_view(),
         name='list_exercise_in_workout'),
    path('<uuid:pk>/', ExerciseInWorkoutRetrieveView.as_view(),
         name='retrieve_exercise_in_workout'),
]

app_name = 'workout'

urlpatterns = [
    path('', WorkoutListView.as_view(), name='list_workouts'),
    path('<uuid:pk>/', WorkoutRetrieveView.as_view(), name='retrieve_workout'),
    path('start/', include(create_workout_urlpatterns)),
    path('unfinished/', GetUnfinishedWorkoutView.as_view(),
         name='unfinished_workout'),
    path('finish/', FinishWorkoutView.as_view(), name='finish_workout'),
    path('approach/', include(approach_urlpatterns)),
    path('exercise/', include(exercise_urlpatterns)),
]
