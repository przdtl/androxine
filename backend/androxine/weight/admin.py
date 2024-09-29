from django.contrib import admin

from weight.models import Weight, UserWorkoutSettings


@admin.register(Weight)
class WeightAdmin(admin.ModelAdmin):
    readonly_fields = ['id']


@admin.register(UserWorkoutSettings)
class UserWorkoutSettingsAdmin(admin.ModelAdmin):
    pass
