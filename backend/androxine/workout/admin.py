from django.contrib import admin

from workout.models import Workout, ExerciseInWorkout, ExerciseApproachInWorkout


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    pass


@admin.register(ExerciseInWorkout)
class ExerciseInWorkoutAdmin(admin.ModelAdmin):
    pass


@admin.register(ExerciseApproachInWorkout)
class ExerciseApproachInWorkoutAdmin(admin.ModelAdmin):
    pass
