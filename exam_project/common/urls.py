from django.urls import path
from exam_project.common.views import bought_games

urlpatterns = (
    path('<int:pk>/', bought_games, name='bought games'), )
