from django.urls import path

from workout_settings.views import UserWorkoutSettingsRetrieveUpdateView, ResetUserWorkoutSettingsView

urlpatterns = [
    path('', UserWorkoutSettingsRetrieveUpdateView.as_view(),
         name='workout_settings'),
    path('reset/', ResetUserWorkoutSettingsView.as_view(),
         name='reset_workout_settings'),
]
