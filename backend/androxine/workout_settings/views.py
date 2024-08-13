from rest_framework.generics import RetrieveUpdateAPIView

from config.utils import CustomGetObjectMixin

from workout_settings.models import UserWorkoutSettings
from workout_settings.serializers import UserWorkoutSettingsSerializer


class UserWorkoutSettingsRetrieveUpdateView(CustomGetObjectMixin, RetrieveUpdateAPIView):
    serializer_class = UserWorkoutSettingsSerializer

    def get_queryset(self):
        return UserWorkoutSettings.objects.filter(
            user_id=self.request.user.pk
        )
