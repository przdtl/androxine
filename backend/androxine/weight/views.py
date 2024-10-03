import datetime

from django.http import Http404

from rest_framework.generics import (
    CreateAPIView,
    GenericAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema

from weight.models import Weight, UserWorkoutSettings
from weight.serializers import (
    WeightTableListSerializer,
    WeightListCreateSerializer,
    WeightCreateSwaggerSerializer,
    UserWorkoutSettingsCreateSerializer,
    WeightRetrieveUpdateDestroySerializer,
    UserWorkoutSettingsCreateSwaggerSerializer,
    UserWorkoutSettingsRetrieveUpdateDestroySerializer,
)

from config.utils import CustomGetObjectMixin, UpdateRequestManager, methods_decorator


class WeightListCreateView(ListCreateAPIView):
    serializer_class = WeightListCreateSerializer

    def get_queryset(self):
        return Weight.objects.filter(
            user=self.request.user
        ).order_by('-date')

    @swagger_auto_schema(
        request_body=WeightCreateSwaggerSerializer,
        responses={201: WeightListCreateSerializer},
    )
    def post(self, request, *args, **kwargs):
        with UpdateRequestManager(request.data):
            request.data.update({'user': request.user.pk})

        return super().post(request, *args, **kwargs)


class WeightRetrieveUpdateDestroyView(CustomGetObjectMixin, RetrieveUpdateDestroyAPIView):
    serializer_class = WeightRetrieveUpdateDestroySerializer
    queryset = Weight.objects.all()
    shadow_user_lookup_field = 'user'
    http_method_names = ['get', 'patch', 'delete']


class WeightTableListView(GenericAPIView):
    serializer_class = WeightTableListSerializer
    pagination_class = None

    def get_queryset(self):
        user_weight_querset = Weight.objects.filter(
            user=self.request.user
        ).order_by('date')
        first_weight_record = user_weight_querset.first()
        if not first_weight_record:
            raise Http404
        
        first_weight_record_date = first_weight_record.date
        dates_range = 1 + int(
            (datetime.date.today() - first_weight_record_date).days
        )
        labels = [
            first_weight_record_date + datetime.timedelta(days=idx) for idx in range(dates_range)
        ]
        values = user_weight_querset.values('body_weight', 'date')

        return {
            "labels": labels,
            "values": values,
        }

    def get(self, request, *args, **kwargs):
        instance = self.get_queryset()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


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
