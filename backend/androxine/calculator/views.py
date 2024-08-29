from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from drf_yasg.utils import swagger_auto_schema

from workout.models import ExerciseApproachInWorkout

from calculator.serializers import CalculateSerializer, CalculateByApproachSerializer
from calculator.services import calculate_one_rep_maximum_weight


class CalculateView(APIView):
    permission_classes = [AllowAny]

    def get_serializer(self, *args, **kwargs):
        return CalculateSerializer(*args, **kwargs)

    @swagger_auto_schema(
        query_serializer=CalculateSerializer
    )
    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        calculated_data = calculate_one_rep_maximum_weight(
            **serializer.data
        )
        if isinstance(calculated_data, tuple):
            response_data = {
                'result': calculated_data[0],
                'functions': calculated_data[1]
            }
        else:
            response_data = {
                'result': calculated_data,
            }

        return Response(response_data, status=status.HTTP_200_OK)


class CalculateByApproachView(APIView):
    def get_serializer(self, *args, **kwargs):
        return CalculateByApproachSerializer(*args, **kwargs)

    @swagger_auto_schema(
        query_serializer=CalculateByApproachSerializer
    )
    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        approach_id = serializer.data.get('approach_id')

        approach = get_object_or_404(
            ExerciseApproachInWorkout,
            pk=approach_id,
        )
        reps = approach.reps
        weight = approach.weight
        only_result = serializer.data.get('only_result')

        calculated_data = calculate_one_rep_maximum_weight(
            reps=reps,
            weight=weight,
            only_result=only_result
        )
        if isinstance(calculated_data, tuple):
            response_data = {
                'result': calculated_data[0],
                'functions': calculated_data[1]
            }
        else:
            response_data = {
                'result': calculated_data,
            }

        return Response(response_data, status=status.HTTP_200_OK)
