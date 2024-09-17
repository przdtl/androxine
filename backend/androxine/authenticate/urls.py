from django.urls import path, include

from authenticate.views import (
    Me,
    get_csrf,
    UserLogin,
    UserLogout,
    UserRegister,
    ActivateUser,
)


urlpatterns = [
    path('oauth/', include('social_django.urls', namespace='social')),
    path('signup/', UserRegister.as_view(), name='signup'),
    path('signin/', UserLogin.as_view(), name='signin'),
    path('signout/', UserLogout.as_view(), name='signout'),
    path('me/', Me.as_view(), name='me'),
    path('activate/<user_id>/<token>', ActivateUser.as_view(), name='activate'),
    path('csrf/', get_csrf, name='get_csrf'),
]
