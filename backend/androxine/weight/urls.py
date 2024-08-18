from django.urls import path

from weight.views import WeightListCreateView, WeightRetrieveUpdateDestroyView

urlpatterns = [
    path('', WeightListCreateView.as_view(), name='list_create_weight'),
    path('<uuid:pk>/', WeightRetrieveUpdateDestroyView.as_view(),
         name='manage_weight'),
]
