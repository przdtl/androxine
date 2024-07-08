from django.urls import path, include

from authenticate.views import login


urlpatterns = [
    path('oauth/', include('social_django.urls', namespace='social')),
    path('login/', login, name='login'),
]
