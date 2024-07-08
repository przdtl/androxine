from django.shortcuts import render

from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.decorators import api_view, permission_classes


@permission_classes([AllowAny])
def login(request: Request):
    return render(request, 'login.html')