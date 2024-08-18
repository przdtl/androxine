from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView

from weight.models import Weight
from weight.serializers import ReadWeightSerializer, WriteWeightSerializer

from config.utils import CustomGetObjectMixin, UpdateRequestManager


class WeightListCreateView(ListCreateAPIView):
    serializer_class = WriteWeightSerializer

    def get_queryset(self):
        return Weight.objects.filter(
            user=self.request.user
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
