from django.shortcuts import render
from exam_project.accounts.models import AppUser
from exam_project.common.models import BoughtGame
from exam_project.games.models import GameModel


def bought_games(request, pk):
    user = AppUser.objects.filter(pk=pk).get()
    # all_bought_games = []
    all_games = BoughtGame.objects.all()
    # for element in all_games:
    #     aa= element.user
    #     a = element.user.pk
    #     c= user.pk
    #     if element.user.pk == user.pk:
    #         all_bought_games.append(GameModel.objects.filter(pk=element.game.pk))
    #     d = all_bought_games[0]

    context = {'all_games': all_games, 'user': user, }

    return render(request, 'bought_games.html', context)
