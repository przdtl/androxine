from django.urls import path

from calculator.views import CalculateView, CalculateByApproachView

app_name = 'calculator'

urlpatterns = [
    path('', CalculateView.as_view(), name='calculate'),
    path('by_approach/', CalculateByApproachView.as_view(),
         name='calculate_by_approach'),
]
