from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import generic as views
from exam_project.accounts.models import AppUser
from exam_project.common.models import BoughtGame
from exam_project.games.forms import GameAddForm, GameEditForm, GameDeleteForm
from exam_project.games.models import GameModel


class IndexView(views.ListView):
    model = GameModel
    template_name = 'home-page.html'
    context_object_name = 'games'


def my_games(request, pk):
    games = []
    all_games = GameModel.objects.all()
    for game in all_games:
        if game.user.pk == pk:
            games.append(game)
    context = {'games': games, }
    return render(request, 'my-games.html', context)


@login_required
def game_add(request):
    if request.method == 'GET':
        form = GameAddForm()
    else:
        form = GameAddForm(request.POST)
        if form.is_valid():
            game = form.save(commit=False)
            game.user = request.user
            game.save()
            return redirect('index')

    context = {
        'form': form,
    }
    return render(request, 'game/create-game.html', context, )


@login_required
def game_details(request, pk):
    game = GameModel.objects.filter(pk=pk).get()
    user = AppUser.objects.filter(pk=request.user.pk).get()
    is_owner = request.user.pk == game.user.pk
    is_bought = BoughtGame.objects.filter(user=user, game=game)

    context = {
        'game': game,
        'is_owner': is_owner,
        'is_bought': is_bought.ordered,
    }
    return render(request, 'game/details-game.html', context, )


def is_unique(game1, user1):
    game = game1
    user = user1

    new_bought_game = BoughtGame.objects.create(user=user, game=game)
    counter = 0
    all_games = BoughtGame.objects.all()
    for bought_game in all_games:
        if bought_game.game == new_bought_game.game and bought_game.user == new_bought_game.user:
            counter += 1
            if counter > 1:
                new_bought_game.delete()
                return False
    return True


@login_required
def game_buy(request, pk):
    game = GameModel.objects.filter(pk=pk).get()
    user = AppUser.objects.filter(pk=request.user.pk).get()
    result = None
    result1 = None

    if user.money >= game.price:
        result = is_unique(game, user)
        result1 = True
        if result:
            user.money -= game.price
            bought = True
            message = 'You bought a game'
            user.save()

            context = {
                'game': game,
                'bought': bought,
                'message': message,
                'user': user,
            }
            return render(request, 'game/buy-game.html', context)

    bought = False
    if result1:
        message = 'Already bought'
    else:
        message = 'Not enough money to buy'

    context = {
        'game': game,
        'bought': bought,
        'message': message,
        'user': user,
    }
    return render(request, 'game/buy-game.html', context)


def game_edit(request, pk):
    game = GameModel.objects.filter(pk=pk).get()

    if request.method == 'GET':
        form = GameEditForm(instance=game)
    else:
        form = GameEditForm(request.POST, instance=game)
        if form.is_valid():
            form.save()
            return redirect('bought games')

    context = {'form': form,
               'game': game, }

    return render(request, 'game/edit-game.html', context)


def game_delete(request, pk):
    game = GameModel.objects.filter(pk=pk).get()

    if request.method == 'GET':
        form = GameDeleteForm(instance=game)
    else:
        form = GameDeleteForm(request.POST, instance=game)
        if form.is_valid():
            form.save()
            return redirect('bought games')

    context = {
        'form': form,
        'game': game,
    }
    return render(request, 'game/delete-game.html', context, )
