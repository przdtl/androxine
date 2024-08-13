from django.db.models.fields import NOT_PROVIDED

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateAPIView

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from config.utils import CustomGetObjectMixin

from workout_settings.models import UserWorkoutSettings
from workout_settings.serializers import UserWorkoutSettingsSerializer


class UserWorkoutSettingsRetrieveUpdateView(CustomGetObjectMixin, RetrieveUpdateAPIView):
    serializer_class = UserWorkoutSettingsSerializer

    def get_queryset(self):
        return UserWorkoutSettings.objects.filter(
            user_id=self.request.user.pk
        )


class ResetUserWorkoutSettingsView(APIView):
    @swagger_auto_schema(
        responses={200: openapi.Response('', UserWorkoutSettingsSerializer)}
    )
    def post(self, request, format=None):
        settings_instance = UserWorkoutSettings.objects.get(pk=request.user.pk)
        for f in settings_instance._meta.fields:
            if f.default != NOT_PROVIDED:
                setattr(settings_instance, f.name, f.default)

        settings_instance.save()
        serializer = UserWorkoutSettingsSerializer(settings_instance)

        return Response(serializer.data, status=status.HTTP_200_OK)
