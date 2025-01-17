from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import login, logout, get_user_model

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from authenticate.tasks import send_user_verifications_email
from authenticate.services import get_user_from_email_verification_token
from authenticate.serializers import SignupSerializer, SigninSerializer, UserReadSerializer, ActivateUserSerializer

UserModel = get_user_model()


def get_csrf(request):
    response = JsonResponse({'detail': 'CSRF cookie set'})
    response['X-CSRFToken'] = get_token(request)
    return response


class UserRegister(CreateAPIView):
    permission_classes = [AllowAny,]
    serializer_class = SignupSerializer

    def perform_create(self, serializer):
        self.user = serializer.save()

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        send_user_verifications_email.delay(self.user.pk)
        return response


class UserLogin(APIView):
    permission_classes = [AllowAny,]

    @swagger_auto_schema(
        request_body=SigninSerializer,
        responses={202: openapi.Response('Success ligin')},
    )
    def post(self, request, format=None):
        serializer = SigninSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        login(request, user)

        return Response(status=status.HTTP_202_ACCEPTED)


class ActivateUser(APIView):
    permission_classes = [AllowAny,]

    def get(self, request, user_id, token):
        serializer = ActivateUserSerializer(
            data={'user_id': user_id, 'token': token})
        serializer.is_valid(raise_exception=True)

        user = get_user_from_email_verification_token(**serializer.data)
        if not user:
            return Response(data={'detail': _('Token is invalid')}, status=status.HTTP_403_FORBIDDEN)

        if user.is_active:
            return Response(data={'detail': _('User is already active')}, status=status.HTTP_400_BAD_REQUEST)

        user.is_active = True
        user.save()
        return Response(status=status.HTTP_200_OK)


class UserLogout(APIView):
    def post(self, request, format=None):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class Me(APIView):
    def get(self, request, format=None):
        serializer_data = UserReadSerializer(request.user).data
        return Response(serializer_data, status=status.HTTP_200_OK)
