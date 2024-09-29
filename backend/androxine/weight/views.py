from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, CreateAPIView

from drf_yasg.utils import swagger_auto_schema

from weight.models import Weight, UserWorkoutSettings
from weight.serializers import (
    ReadWeightSerializer,
    WriteWeightSerializer,
    WeightCreateSwaggerSerializer,
    UserWorkoutSettingsCreateSerializer,
    UserWorkoutSettingsCreateSwaggerSerializer,
    UserWorkoutSettingsRetrieveUpdateDestroySerializer,
)

from config.utils import CustomGetObjectMixin, UpdateRequestManager, methods_decorator


class WeightListCreateView(ListCreateAPIView):
    serializer_class = WriteWeightSerializer

    def get_queryset(self):
        return Weight.objects.filter(
            user=self.request.user
        )

    @swagger_auto_schema(
        request_body=WeightCreateSwaggerSerializer,
        responses={201: WriteWeightSerializer},
    )
    def post(self, request, *args, **kwargs):
        with UpdateRequestManager(request.data):
            request.data.update({'user': request.user.pk})

        return super().post(request, *args, **kwargs)


class WeightRetrieveUpdateDestroyView(CustomGetObjectMixin, RetrieveUpdateDestroyAPIView):
    serializer_class = ReadWeightSerializer
    queryset = Weight.objects.all()
    shadow_user_lookup_field = 'user'
    http_method_names = ['get', 'patch', 'delete']


class UserWorkoutSettingsCreateView(CreateAPIView):
    serializer_class = UserWorkoutSettingsCreateSerializer

    @swagger_auto_schema(
        request_body=UserWorkoutSettingsCreateSwaggerSerializer,
        responses={201: UserWorkoutSettingsCreateSerializer},
        tags=['weight_settings'],
    )
    def post(self, request, *args, **kwargs):
        with UpdateRequestManager(request.data):
            request.data.update({'user': request.user.pk})

        return super().post(request, *args, **kwargs)


@methods_decorator(swagger_auto_schema(tags=['weight_settings']), names=['get', 'patch', 'delete'])
class UserWorkoutSettingsRetrieveUpdateDestroyView(CustomGetObjectMixin, RetrieveUpdateDestroyAPIView):
    serializer_class = UserWorkoutSettingsRetrieveUpdateDestroySerializer
    queryset = UserWorkoutSettings.objects.all()
    shadow_user_lookup_field = 'user'
    http_method_names = ['get', 'patch', 'delete']
