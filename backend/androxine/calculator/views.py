from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from drf_yasg.utils import swagger_auto_schema

from calculator.serializers import CalculateSerializer
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
        result, intermediate_calculations = calculate_one_rep_maximum_weight(
            **serializer.data, only_result=False
        )
        response_data = {
            'result': result,
            'functions': intermediate_calculations
        }

        return Response(response_data, status=status.HTTP_200_OK)


class CalculateByApproachView(APIView):
    pass
