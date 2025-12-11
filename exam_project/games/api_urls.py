from django.urls import path
from .api_views import (
    GamesListCreateApiView,
    GameRetrieveUpdateDeleteApiView,
    MyGamesListApiView,
    GameBuyApiView,
)

urlpatterns = [
    path('', GamesListCreateApiView.as_view(), name='games_list_create'),
    path('mine/', MyGamesListApiView.as_view(), name='games_mine'),
    path('<int:pk>/', GameRetrieveUpdateDeleteApiView.as_view(), name='games_detail'),
    path('<int:pk>/buy/', GameBuyApiView.as_view(), name='games_buy'),
]
