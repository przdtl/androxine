from django.shortcuts import render
from django.forms.models import model_to_dict
from django.contrib.auth import login, logout, get_user_model
from django.utils.translation import gettext_lazy as _

from rest_framework.request import Request
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from authenticate.serializers import SignupSerializer, SigninSerializer, UserReadSerializer
from authenticate.services import get_user_from_email_verification_token
from authenticate.tasks import send_user_verifications_email

UserModel = get_user_model()


@permission_classes([AllowAny])
def login_view(request: Request):
    return render(request, 'authenticate/login.html')


class UserRegister(CreateAPIView):
    permission_classes = [AllowAny,]
    serializer_class = SignupSerializer

    def perform_create(self, serializer):
        self.user = serializer.save()

    def post(self, request: Request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        send_user_verifications_email.delay(self.user.pk, request.get_host())
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

    def get(self, request, uid, token):
        user = get_user_from_email_verification_token(uid, token)
        if not user:
            return Response(data={'detail': _('Token is invalid')}, status=status.HTTP_403_FORBIDDEN)

        if user.is_active:
            return Response(data={'detail': _('User is already active')}, status=status.HTTP_400_BAD_REQUEST)

        user.is_active = True
        user.save()
        return Response(status=status.HTTP_200_OK)


class UserLogout(APIView):
    def get(self, request, format=None):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class Me(APIView):
    def get(self, request, format=None):
        data = model_to_dict(request.user)
        data.update(id=request.user.pk)
        serializer_data = UserReadSerializer(data).data
        return Response(serializer_data, status=status.HTTP_202_ACCEPTED)
