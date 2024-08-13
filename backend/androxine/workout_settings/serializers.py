from rest_framework import serializers

from workout_settings.models import UserWorkoutSettings


class UserWorkoutSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserWorkoutSettings
        fields = '__all__'
        read_only_fields = ['user']
