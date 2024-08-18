from rest_framework import serializers

from weight.models import Weight


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
            field for field in fields if field != 'body_weight']
