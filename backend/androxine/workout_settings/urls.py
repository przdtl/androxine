from django.urls import path

from workout_settings.views import UserWorkoutSettingsRetrieveUpdateView

urlpatterns = [
    path('', UserWorkoutSettingsRetrieveUpdateView.as_view(), name='workout_settings')
]
