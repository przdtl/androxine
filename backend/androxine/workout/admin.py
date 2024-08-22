from django.contrib import admin

from workout.models import Workout, ExerciseInWorkout, ExerciseApproachInWorkout


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    readonly_fields = ['id', 'beginning_datetime']


@admin.register(ExerciseInWorkout)
class ExerciseInWorkoutAdmin(admin.ModelAdmin):
    readonly_fields = ['id']


@admin.register(ExerciseApproachInWorkout)
class ExerciseApproachInWorkoutAdmin(admin.ModelAdmin):
    readonly_fields = ['id']
