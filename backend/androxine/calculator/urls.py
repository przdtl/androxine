from django.urls import path

from calculator.views import CalculateView, CalculateByApproachView

urlpatterns = [
    path('', CalculateView.as_view(), name='calculate'),
    path('by_approach/<uuid:pk>', CalculateByApproachView.as_view(),
         name='calculate_by_approach'),
]
