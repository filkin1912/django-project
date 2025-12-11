from django.urls import path
from .api_views import MeRetrieveUpdateApiView, UsersListApiView, SignUpApiView

urlpatterns = [
    path('me/', MeRetrieveUpdateApiView.as_view(), name='accounts_me'),
    path('users/', UsersListApiView.as_view(), name='accounts_users'),
    path('signup/', SignUpApiView.as_view(), name='accounts_signup'),
]
