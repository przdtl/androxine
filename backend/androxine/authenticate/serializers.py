from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password

UserModel = get_user_model()


class SigninSerializer(serializers.Serializer):

    username = serializers.CharField(write_only=True,)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(request=self.context.get('request'),
                            username=username, password=password)

        if not user:
            msg = 'Access denied: wrong username or password.'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return super().validate(attrs)


class SignupSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=UserModel.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = UserModel
        fields = ['username', 'email', 'password', 'password2',]

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = UserModel(
            username=validated_data['username'],
            email=validated_data['email'],
            is_active=False,
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
