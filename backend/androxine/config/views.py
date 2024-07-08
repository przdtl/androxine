from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny


@api_view(['GET'])
def foo(request: Request):
    return Response({'msg': 'ok'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny,])
def boo(request: Request):
    return Response({'message': 'ooook'}, status=status.HTTP_200_OK)
