from django.urls import path, include

from weight.views import (
    WeightTableListView,
    WeightListCreateView,
    UserWorkoutSettingsCreateView,
    WeightRetrieveUpdateDestroyView,
    UserWorkoutSettingsRetrieveUpdateDestroyView,
)

weight_urlpatterns = [
    path('', WeightListCreateView.as_view(), name='list_create_weight'),
    path('table/', WeightTableListView.as_view(), name='table_list_weight'),
    path('<uuid:pk>/', WeightRetrieveUpdateDestroyView.as_view(),
         name='manage_weight'),
]

weight_settings_urlpatterns = [
    path('', UserWorkoutSettingsCreateView.as_view(),
         name='list_create_weight_settings'),
    path('me/', UserWorkoutSettingsRetrieveUpdateDestroyView.as_view(),
         name='manage_weight_settings'),
]

urlpatterns = [
    path('settings/', include(weight_settings_urlpatterns)),
    path('', include(weight_urlpatterns)),
]
