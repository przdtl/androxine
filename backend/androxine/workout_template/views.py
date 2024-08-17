from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from drf_yasg.utils import swagger_auto_schema

from config.utils import UpdateRequestManager

from workout_template.models import (
    WorkoutTemplate,
    ExerciseInWorkoutTemplate,
    ExerciseApproachInWorkoutTemplate,
)
from workout_template.serializers import (
    WorkoutTemplateWriteSerializer,
    WorkoutTemplateReadSerializer,
    ExerciseInWorkoutTemplateWriteSerializer,
    ExerciseInWorkoutTemplateReadSerializer,
    ExerciseApproachInWorkoutTemplateWriteSerializer,
    ExerciseApproachInWorkoutTemplateReadSerializer,
)


class WorkoutTemplateCreateListView(ListCreateAPIView):
    serializer_class = WorkoutTemplateWriteSerializer

    def get_queryset(self):
        user_id = self.request.user.pk
        return WorkoutTemplate.objects.filter(
            created_by__id=user_id
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


class ExerciseInWorkoutTemplateCreateListView(ListCreateAPIView):
    serializer_class = ExerciseInWorkoutTemplateWriteSerializer

    def get_queryset(self):
        user_id = self.request.user.pk
        return ExerciseInWorkoutTemplate.objects.filter(
            template__created_by__id=user_id
        )

    @swagger_auto_schema(tags=['template_exercise'])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    @swagger_auto_schema(tags=['template_exercise'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ExerciseInWorkoutTemplateRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = ExerciseInWorkoutTemplateReadSerializer
    queryset = ExerciseInWorkoutTemplate.objects.all()

    def get_object(self):
        instance = super().get_object()
        if instance.template.created_by.pk != self.request.user.pk:
            raise PermissionDenied()

        return instance

    @swagger_auto_schema(tags=['template_exercise'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(tags=['template_exercise'])
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(tags=['template_exercise'])
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(tags=['template_exercise'])
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class ExerciseApproachInWorkoutTemplateCreateListView(ListCreateAPIView):
    serializer_class = ExerciseApproachInWorkoutTemplateWriteSerializer

    def get_queryset(self):
        user_id = self.request.user.pk
        return ExerciseApproachInWorkoutTemplate.objects.filter(
            exercise_in_workout_template__template__created_by__id=user_id
        )

    @swagger_auto_schema(tags=['template_exercise_approach'])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    @swagger_auto_schema(tags=['template_exercise_approach'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ExerciseApproachInWorkoutTemplateRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = ExerciseApproachInWorkoutTemplateReadSerializer
    queryset = ExerciseApproachInWorkoutTemplate.objects.all()

    def get_object(self):
        instance = super().get_object()
        if instance.exercise_in_workout_template.template.created_by.pk != self.request.user.pk:
            raise PermissionDenied()

        return instance

    @swagger_auto_schema(tags=['template_exercise_approach'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(tags=['template_exercise_approach'])
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(tags=['template_exercise_approach'])
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(tags=['template_exercise_approach'])
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
