from django.contrib import admin

from exercise.models import Exercise, ExerciseCategory, UserExerciseSettings


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    readonly_fields = ['id', 'slug']


@admin.register(ExerciseCategory)
class ExerciseCategoryAdmin(admin.ModelAdmin):
    readonly_fields = ['id', 'slug']


@admin.register(UserExerciseSettings)
class UserExerciseSettingsAdmin(admin.ModelAdmin):
    readonly_fields = ['id']
