from django.urls import path, include

from authenticate.views import login_view, UserLogin, UserRegister, ActivateUser


urlpatterns = [
    path('oauth/', include('social_django.urls', namespace='social')),
    path('signup/', UserRegister.as_view(), name='signup'),
    path('signin/', UserLogin.as_view(), name='signin'),
    path('activate/<uid>/<token>', ActivateUser.as_view(), name='activate'),
    path('login_template/', login_view, name='login'),
]
