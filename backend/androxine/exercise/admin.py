from django.contrib import admin

from exercise.models import Exercise, ExerciseCategory, UserExerciseSettings


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    exclude = ['slug']
    readonly_fields = ['id']


@admin.register(ExerciseCategory)
class ExerciseCategoryAdmin(admin.ModelAdmin):
    exclude = ['slug']
    readonly_fields = ['id']


@admin.register(UserExerciseSettings)
class UserExerciseSettingsAdmin(admin.ModelAdmin):
    readonly_fields = ['id']
