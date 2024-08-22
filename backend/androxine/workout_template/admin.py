from django.contrib import admin

from workout_template.models import (
    WorkoutTemplate,
    ExerciseInWorkoutTemplate,
    ExerciseApproachInWorkoutTemplate
)


@admin.register(WorkoutTemplate)
class WorkoutTemplateAdmin(admin.ModelAdmin):
    readonly_fields = ['id']


@admin.register(ExerciseInWorkoutTemplate)
class ExerciseInWorkoutTemplateAdmin(admin.ModelAdmin):
    readonly_fields = ['ordinal_number', 'id']


@admin.register(ExerciseApproachInWorkoutTemplate)
class ExerciseApproachInWorkoutTemplateAdmin(admin.ModelAdmin):
    readonly_fields = ['ordinal_number', 'id']
