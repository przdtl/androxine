from django.contrib import admin

from workout_template.models import WorkoutTemplate, ExerciseInWorkoutTemplate, ExerciseApproachInWorkoutTemplate


@admin.register(WorkoutTemplate)
class WorkoutTemplateAdmin(admin.ModelAdmin):
    pass


@admin.register(ExerciseInWorkoutTemplate)
class ExerciseInWorkoutTemplateAdmin(admin.ModelAdmin):
    readonly_fields = ['ordinal_number']


@admin.register(ExerciseApproachInWorkoutTemplate)
class ExerciseApproachInWorkoutTemplateAdmin(admin.ModelAdmin):
    readonly_fields = ['ordinal_number']
