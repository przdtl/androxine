from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from weight.models import Weight, UserWorkoutSettings


class WeightCreateSwaggerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weight
        fields = ['body_weight', 'description']


class ReadWeightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weight
        fields = '__all__'
        read_only_fields = ['id', 'user', 'date']


class WriteWeightSerializer(serializers.ModelSerializer):
    user = serializers.UUIDField(
        source='user_id',
        required=False,
        help_text='this field is calculated automatically based on the data of the logged-in user',
    )

    class Meta:
        model = Weight
        fields = '__all__'
        read_only_fields = [
            field for field in fields if field not in ('body_weight', 'description')]


class UserWorkoutSettingsCreateSwaggerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserWorkoutSettings
        fields = ['started_weight', 'desired_weight']


class UserWorkoutSettingsRetrieveUpdateDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserWorkoutSettings
        fields = '__all__'
        read_only_fields = ['user']


class UserWorkoutSettingsCreateSerializer(serializers.ModelSerializer):
    user = serializers.UUIDField(
        source='user_id',
        required=False,
        help_text='this field is calculated automatically based on the data of the logged-in user',
        validators=[UniqueValidator(UserWorkoutSettings.objects.all())]
    )

    class Meta:
        model = UserWorkoutSettings
        fields = '__all__'
