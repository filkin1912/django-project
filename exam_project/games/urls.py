from django.urls import path, include
from exam_project.games.views import game_add, game_details, game_edit, game_delete, my_games, \
    game_buy, IndexView

urlpatterns = (
    path('', IndexView.as_view(), name='index'),
    # path('dashboard/', BoughtGamesView.as_view(), name='bought games'),
    path('my_games/<int:pk>/', my_games, name='my games'),
    path('game/', include([
        path('create/', game_add, name='game create'),
        path('details/<int:pk>/', game_details, name='game details'),
        path('edit/<int:pk>/', game_edit, name='game edit'),
        path('delete/<int:pk>/', game_delete, name='game delete'),
        path('buy/<int:pk>/', game_buy, name='game buy')
    ]))
)
