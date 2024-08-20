import datetime

from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    GenericAPIView,
    RetrieveAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from drf_yasg.utils import swagger_auto_schema, no_body

from config.utils import UpdateRequestManager

from workout_template.models import ExerciseApproachInWorkoutTemplate

from workout.models import (
    Workout, ExerciseInWorkout, ExerciseApproachInWorkout
)
from workout.serializers import (
    WorkoutReadSerializer,
    WorkoutIdSwaggerSerializer,
    ExerciseInWorkoutSerializer,
    WorkoutCreateSwaggerSerializer,
    WorkoutIsOverSwaggerSerializer,
    WorkoutCreateByTemplateSerializer,
    ExerciseApproachInWorkoutSerializer,
    ApproachByTemplateSwaggerSerializer,
    WorkoutCreateByTemplateSwaggerSerializer,
    ExerciseInWorkoutCreateSwaggerSerializer,
)
from workout.utils import is_exists_non_finished_workout, calculate_absolute_weight_from_relative


class WorkoutListView(ListAPIView):
    serializer_class = WorkoutReadSerializer

    def get_queryset(self):
        input_serializer = WorkoutIsOverSwaggerSerializer(
            data=self.request.query_params
        )
        input_serializer.is_valid(raise_exception=True)
        filter_data = {
            'created_by__id': self.request.user.pk,
        }
        is_over_only = input_serializer.data.get('is_over_only')
        if is_over_only:
            filter_data.update({'enging_datetime__isnull': False})

        return Workout.objects.filter(**filter_data)

    @swagger_auto_schema(
        query_serializer=WorkoutIsOverSwaggerSerializer
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class WorkoutCreateView(CreateAPIView):
    serializer_class = WorkoutReadSerializer

    @swagger_auto_schema(
        request_body=WorkoutCreateSwaggerSerializer
    )
    def post(self, request, *args, **kwargs):
        is_exists_non_finished_workout = Workout.objects.filter(
            enging_datetime__isnull=True
        ).exists()
        if is_exists_non_finished_workout:
            raise ValidationError(
                "You can't start a new workout until you finish a workout you've already started"
            )

        with UpdateRequestManager(request.data):
            request.data.update({'created_by': request.user.pk})

        return super().post(request, *args, **kwargs)


class WorkoutCreateByTemplateView(CreateAPIView):
    serializer_class = WorkoutCreateByTemplateSerializer

    @swagger_auto_schema(
        query_serializer=WorkoutCreateByTemplateSwaggerSerializer,
        request_body=no_body,
    )
    def post(self, request, *args, **kwargs):
        if is_exists_non_finished_workout():
            raise ValidationError(
                "You can't start a new workout until you finish a workout you've already started"
            )

        input_serializer = WorkoutCreateByTemplateSwaggerSerializer(
            data=request.query_params
        )
        input_serializer.is_valid(raise_exception=True)
        workout_template_id = input_serializer.data.get('workout_template')

        workout_template = get_object_or_404(Workout, pk=workout_template_id)
        break_between_approaches = workout_template.break_between_approaches
        created_by = request.user.pk

        data = {
            'workout_template': workout_template,
            'break_between_approaches': break_between_approaches,
            'created_by': created_by,
        }

        with UpdateRequestManager(request.data):
            request.data.update(data)

        return super().post(request, *args, **kwargs)


class GetUnfinishedWorkoutView(APIView):
    def get_serializer(self, **kwargs):
        return WorkoutReadSerializer(**kwargs)

    def get(self, request, *args, **kwargs):
        workout_template = get_object_or_404(
            Workout,
            created_by_id=request.user.pk,
            enging_datetime__isnull=True
        )
        serializer_data = self.get_serializer(instance=workout_template).data

        return Response(serializer_data, status=status.HTTP_200_OK)


class FinishWorkoutView(APIView):
    def get_serializer(self, **kwargs):
        return WorkoutReadSerializer(**kwargs)

    @swagger_auto_schema(
        request_body=no_body,
    )
    def post(self, request, *args, **kwargs):
        workout_template = get_object_or_404(
            Workout,
            created_by_id=request.user.pk,
            enging_datetime__isnull=True
        )
        workout_template.enging_datetime = datetime.datetime.now()
        workout_template.save()

        serializer_data = self.get_serializer(instance=workout_template).data

        return Response(serializer_data, status=status.HTTP_200_OK)


class WorkoutRetrieveView(RetrieveAPIView):
    serializer_class = WorkoutReadSerializer

    def get_queryset(self):
        return Workout.objects.filter(
            created_by__id=self.request.user.pk
        )


class ApproachByTemplateCreateView(CreateAPIView):
    serializer_class = ExerciseApproachInWorkoutSerializer

    @swagger_auto_schema(
        query_serializer=ApproachByTemplateSwaggerSerializer,
        request_body=no_body,
    )
    def post(self, request, *args, **kwargs):
        if not is_exists_non_finished_workout():
            raise ValidationError(
                "You can't add an approach because you don't have any workouts started."
            )

        input_serializer = ApproachByTemplateSwaggerSerializer(
            data=request.query_params
        )
        input_serializer.is_valid(raise_exception=True)
        template_approach_id = input_serializer.data.get('id')
        template_approach = get_object_or_404(
            ExerciseApproachInWorkoutTemplate,
            pk=template_approach_id,
            relative_weight__isnull=False,
        )
        current_workout = Workout.objects.filter(
            enging_datetime__isnull=True
        )
        exercise = template_approach.exercise_in_workout_template.exercise
        exercise_in_workout, created = ExerciseInWorkout.objects.get_or_create(
            workout=current_workout,
            exercise=exercise,
        )

        weight = calculate_absolute_weight_from_relative(template_approach_id)
        reps = template_approach.reps

        data = {
            'exercise_in_workout': exercise_in_workout,
            'weight': weight,
            'reps': reps,
        }

        with UpdateRequestManager(request.data):
            request.data.update(data)

        return super().post(request, *args, **kwargs)


class ApproachListCreateView(CreateAPIView):
    serializer_class = ExerciseApproachInWorkoutSerializer


class ExerciseInWorkoutListView(ListCreateAPIView):
    serializer_class = ExerciseInWorkoutSerializer

    def get_queryset(self):
        input_serializer = WorkoutIdSwaggerSerializer(
            data=self.request.query_params
        )
        input_serializer.is_valid(raise_exception=True)
        workout_id = input_serializer.data.get('workout_id')
        workout = get_object_or_404(
            Workout,
            id=workout_id,
            created_by=self.request.user.pk,
        )

        return ExerciseInWorkout.objects.filter(workout=workout)

    @swagger_auto_schema(
        query_serializer=WorkoutIdSwaggerSerializer
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=ExerciseInWorkoutCreateSwaggerSerializer,
    )
    def post(self, request, *args, **kwargs):
        current_workout = get_object_or_404(
            Workout, enging_datetime__isnull=True
        )
        with UpdateRequestManager(request.data):
            request.data.update({'workout': current_workout.id})

        return super().post(request, *args, **kwargs)


class ExerciseInWorkoutRetrieveView(ListModelMixin,
                                    RetrieveModelMixin,
                                    GenericAPIView):
    serializer_class = ExerciseApproachInWorkoutSerializer
    queryset = ExerciseInWorkout.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        instance = self.get_object()
        approaches = instance.approaches.all()

        queryset = self.filter_queryset(approaches)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ApproachRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = ExerciseApproachInWorkoutSerializer
    queryset = ExerciseApproachInWorkout.objects.all()


# class NextApproachView(APIView):
#     pass


# class PreviousApproachView(APIView):
#     pass


# class NextExerciseView(APIView):
#     pass


# class PreviousExerciseView(APIView):
#     pass
