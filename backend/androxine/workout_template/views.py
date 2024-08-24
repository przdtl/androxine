from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from drf_yasg.utils import swagger_auto_schema

from config.utils import UpdateRequestManager, methods_decorator

from workout_template.models import (
    WorkoutTemplate,
    ExerciseInWorkoutTemplate,
    ExerciseApproachInWorkoutTemplate,
)
from workout_template.serializers import (
    WorkoutTemplateCreateSwaggerSerializer,
    WorkoutTemplateReadSerializer,
    WorkoutTemplateListCreateSerializer,
    ExerciseInWorkoutTemplateReadSerializer,
    ExerciseInWorkoutTemplateWriteSerializer,
    ExerciseInWorkoutTemplateOrderSerializer,
    ExerciseInWorkoutTemplateReorderSerializer,
    ExerciseApproachInWorkoutTemplateReadSerializer,
    ExerciseApproachInWorkoutTemplateOrderSerializer,
    TemplateIdForExerciseInWorkoutTemplateSerializer,
    ExerciseApproachInWorkoutTemplateWriteSerializer,
    ExerciseApproachInWorkoutTemplateReorderSerializer,
    ExerciseInTemplateIdForExerciseApproachInWorkoutTemplateSerializer,
)


class WorkoutTemplateCreateListView(ListCreateAPIView):
    serializer_class = WorkoutTemplateListCreateSerializer

    def get_queryset(self):
        return WorkoutTemplate.objects.filter(
            created_by__id=self.request.user.pk
        )

    @swagger_auto_schema(
        request_body=WorkoutTemplateCreateSwaggerSerializer,
        responses={201: WorkoutTemplateListCreateSerializer},
    )
    def post(self, request, *args, **kwargs):
        with UpdateRequestManager(request.data):
            request.data.update({'created_by': request.user.pk})

        return super().post(request, *args, **kwargs)


class WorkoutTemplateRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = WorkoutTemplateReadSerializer
    queryset = WorkoutTemplate.objects.all()

    def get_object(self):
        instance = super().get_object()
        if instance.created_by.pk != self.request.user.pk:
            raise PermissionDenied()

        return instance


@methods_decorator(swagger_auto_schema(tags=['template_exercise']), names=['post'])
class ExerciseInWorkoutTemplateCreateListView(ListCreateAPIView):
    serializer_class = ExerciseInWorkoutTemplateWriteSerializer

    def get_queryset(self):
        input_serializer = TemplateIdForExerciseInWorkoutTemplateSerializer(
            data=self.request.query_params,
        )
        input_serializer.is_valid(raise_exception=True)
        template_id = input_serializer.data.get('template_id')
        template = get_object_or_404(
            WorkoutTemplate,
            pk=template_id,
            created_by__id=self.request.user.pk
        )

        return ExerciseInWorkoutTemplate.objects.filter(
            template=template
        )

    @swagger_auto_schema(
        tags=['template_exercise'],
        query_serializer=TemplateIdForExerciseInWorkoutTemplateSerializer,
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


@methods_decorator(swagger_auto_schema(tags=['template_exercise']), names=['delete', 'get', 'put', 'patch'])
class ExerciseInWorkoutTemplateRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = ExerciseInWorkoutTemplateReadSerializer
    queryset = ExerciseInWorkoutTemplate.objects.all()

    def get_object(self):
        instance = super().get_object()
        if instance.template.created_by.pk != self.request.user.pk:
            raise PermissionDenied()

        return instance


class ExerciseInWorkoutTemplateReorderView(APIView):
    def get_serializer(self, *args, **kwargs):
        return ExerciseInWorkoutTemplateReorderSerializer(*args, **kwargs)

    @swagger_auto_schema(
        request_body=ExerciseInWorkoutTemplateReorderSerializer,
        tags=['template_exercise'],
    )
    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        exercises_list = serializer.data.get('exercises')
        template_id = serializer.data.get('template')

        template = get_object_or_404(WorkoutTemplate, pk=template_id)
        exercises = ExerciseInWorkoutTemplate.objects.filter(template=template)

        if len(exercises) != len(exercises_list):
            raise ValidationError({
                'exercises': 'The wrong number of exercise objects was passed, expected: {}, were passed: {}'.format(
                    len(exercises), len(exercises_list))
            })

        exercises_set = set()
        for exercise_dict in exercises_list:
            exercise_pk = exercise_dict['id']
            is_present = ExerciseInWorkoutTemplate.objects.filter(
                id=exercise_pk,
                template=template,
            ).exists()
            if not is_present or exercise_pk in exercises_set:
                raise ValidationError({
                    'exercises': 'Invalid exercise IDs were passed'
                })
            exercises_set.add(exercise_pk)

        exercises_response_data = []
        for exercise_dict in exercises_list:
            exercise_pk = exercise_dict['id']
            new_exercise_number = exercise_dict['ordinal_number']

            exercise = ExerciseInWorkoutTemplate.objects.get(
                pk=exercise_pk
            )
            exercise.ordinal_number = new_exercise_number
            exercise.save()
            exercises_response_data.append(exercise)

        exercises_data = ExerciseInWorkoutTemplateOrderSerializer(
            instance=exercises_response_data, many=True
        ).data
        response_data = {
            'exercises': exercises_data,
            'template': template.id,
        }

        return Response(response_data, status=status.HTTP_200_OK)


@methods_decorator(swagger_auto_schema(tags=['template_exercise_approach']), names=['post'])
class ExerciseApproachInWorkoutTemplateCreateListView(ListCreateAPIView):
    serializer_class = ExerciseApproachInWorkoutTemplateWriteSerializer

    def get_queryset(self):
        input_serializer = ExerciseInTemplateIdForExerciseApproachInWorkoutTemplateSerializer(
            data=self.request.query_params,
        )
        input_serializer.is_valid(raise_exception=True)
        exercise_in_template_id = input_serializer.data.get(
            'exercise_in_template_id')
        exercise_in_template = get_object_or_404(
            ExerciseInWorkoutTemplate,
            pk=exercise_in_template_id,
            template__created_by__id=self.request.user.pk
        )

        return ExerciseApproachInWorkoutTemplate.objects.filter(
            exercise_in_workout_template=exercise_in_template,
        )

    @swagger_auto_schema(
        tags=['template_exercise_approach'],
        query_serializer=ExerciseInTemplateIdForExerciseApproachInWorkoutTemplateSerializer,
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


@methods_decorator(swagger_auto_schema(tags=['template_exercise_approach']), names=['delete', 'get', 'put', 'patch'])
class ExerciseApproachInWorkoutTemplateRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = ExerciseApproachInWorkoutTemplateReadSerializer
    queryset = ExerciseApproachInWorkoutTemplate.objects.all()

    def get_object(self):
        instance = super().get_object()
        if instance.exercise_in_workout_template.template.created_by.pk != self.request.user.pk:
            raise PermissionDenied()

        return instance


class ExerciseApproachInWorkoutTemplateReorderView(APIView):
    def get_serializer(self, *args, **kwargs):
        return ExerciseApproachInWorkoutTemplateReorderSerializer(*args, **kwargs)

    @swagger_auto_schema(
        request_body=ExerciseApproachInWorkoutTemplateReorderSerializer,
        tags=['template_exercise_approach'],
    )
    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        approaches_list = serializer.data.get('approaches')
        exercise_in_template_id = serializer.data.get('exercise_in_template')

        exercise_in_template = get_object_or_404(
            ExerciseInWorkoutTemplate,
            pk=exercise_in_template_id
        )
        approaches = ExerciseApproachInWorkoutTemplate.objects.filter(
            exercise_in_workout_template=exercise_in_template
        )
        if len(approaches) != len(approaches_list):
            raise ValidationError({
                'approaches': 'The wrong number of approaches objects was passed, expected: {}, were passed: {}'.format(
                    len(approaches), len(approaches_list))
            })

        approaches_set = set()
        for approache_dict in approaches_list:
            approache_pk = approache_dict['id']
            is_present = ExerciseApproachInWorkoutTemplate.objects.filter(
                id=approache_pk,
                exercise_in_workout_template=exercise_in_template,
            ).exists()
            if not is_present or approache_pk in approaches_set:
                raise ValidationError({
                    'approaches': 'Invalid exercise IDs were passed'
                })
            approaches_set.add(approache_pk)

        approaches_response_data = []
        for approache_dict in approaches_list:
            approache_pk = approache_dict['id']
            new_approache_number = approache_dict['ordinal_number']

            approache = ExerciseApproachInWorkoutTemplate.objects.get(
                pk=approache_pk
            )
            approache.ordinal_number = new_approache_number
            approache.save()
            approaches_response_data.append(approache)

        approaches_data = ExerciseApproachInWorkoutTemplateOrderSerializer(
            instance=approaches_response_data, many=True
        ).data
        response_data = {
            'approaches': approaches_data,
            'exercise_in_template': approache.id,
        }

        return Response(response_data, status=status.HTTP_200_OK)
