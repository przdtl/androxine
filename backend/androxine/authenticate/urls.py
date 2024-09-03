from django.urls import path, include

from authenticate.views import (
    login_view, UserLogin,
    UserRegister, ActivateUser, Me, UserLogout
)


urlpatterns = [
    path('oauth/', include('social_django.urls', namespace='social')),
    path('signup/', UserRegister.as_view(), name='signup'),
    path('signin/', UserLogin.as_view(), name='signin'),
    path('signout/', UserLogout.as_view(), name='signout'),
    path('me/', Me.as_view(), name='me'),
    path('activate/<user_id>/<token>', ActivateUser.as_view(), name='activate'),
    path('login_template/', login_view, name='login'),
]
