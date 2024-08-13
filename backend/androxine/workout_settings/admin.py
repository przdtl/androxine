from django.contrib import admin

from workout_settings.models import UserWorkoutSettings


@admin.register(UserWorkoutSettings)
class UserWorkoutSettingsAdmin(admin.ModelAdmin):
    pass
