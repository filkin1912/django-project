from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic as views
from exam_project.accounts.models import AppUser
from exam_project.common.models import BoughtGame
from exam_project.games.forms import GameAddForm, GameEditForm, GameDeleteForm
from exam_project.games.models import GameModel
from exam_project.common.models import GameComment
from exam_project.common.forms import GameCommentForm


class IndexView(views.ListView):
    model = GameModel
    template_name = 'home-page.html'
    context_object_name = 'games'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(title__icontains=query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add logged-in user explicitly
        if self.request.user.is_authenticated:
            context['user'] = self.request.user
            context['profile_money'] = self.request.user.money

        query = self.request.GET.get('q')
        context['search_query'] = query or ''

        # Distinguish between no games vs no matches
        total_games = GameModel.objects.count()
        if total_games == 0:
            context['no_games_yet'] = True
        elif query and not context['games']:
            context['no_match'] = True

        return context


class BoughtGamesView(LoginRequiredMixin, views.ListView):
    model = BoughtGame
    template_name = 'bought_games.html'
    context_object_name = 'bought_games'

    def get_queryset(self):
        # Only return games bought by the logged-in user
        return BoughtGame.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hide_buttons'] = True  # ✅ add flag
        return context


def my_games(request, pk):
    games = []
    all_games = GameModel.objects.all()
    for game in all_games:
        if game.user.pk == pk:
            games.append(game)
    context = {'games': games, 'hide_button_buy': True, }
    return render(request, 'my-games.html', context)


@login_required
def game_add(request):
    if request.method == 'GET':
        form = GameAddForm()
    else:
        form = GameAddForm(request.POST, request.FILES)
        if form.is_valid():
            game = form.save(commit=False)
            game.user = request.user
            game.save()
            return redirect('index')
        else:
            print(form.errors)

    context = {
        'form': form,
    }
    return render(request, 'game/create-game.html', context, )


@login_required
def game_details(request, pk):
    game = get_object_or_404(GameModel, pk=pk)
    user = request.user
    is_owner = user == game.user
    is_bought = BoughtGame.objects.filter(user=user, game=game).exists()

    existing_comment = GameComment.objects.filter(game=game, user=user).first()
    form = None

    if request.method == 'POST' and not existing_comment:
        form = GameCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = user
            comment.game = game
            comment.save()
            return redirect('game details', pk=pk)
    elif not existing_comment:
        form = GameCommentForm()

    comments = GameComment.objects.filter(game=game)

    context = {
        'game': game,
        'is_owner': is_owner,
        'is_bought': is_bought,
        'form': form,
        'existing_comment': existing_comment,
        'comments': comments,
    }
    return render(request, 'game/details-game.html', context)


@login_required
def game_buy(request, pk):
    game = get_object_or_404(GameModel, pk=pk)
    user = request.user

    # Prevent buying own game
    if game.user == user:
        messages.error(request, "You cannot buy your own game.")
        return redirect("index")

    # Prevent duplicate purchase
    if BoughtGame.objects.filter(user=user, game=game).exists():
        messages.warning(request, "You already own this game.")
        return redirect("index")

    # Check balance
    if user.money < game.price:
        messages.error(request, "Not enough money to buy this game.")
        return redirect("index")

    # Deduct money and save purchase
    user.money -= game.price
    user.save()
    BoughtGame.objects.create(user=user, game=game)

    messages.success(request, f"You bought {game.title} successfully!")
    return redirect("bought games")


@login_required
def game_edit(request, pk):
    game = GameModel.objects.get(pk=pk)

    if request.method == 'GET':
        form = GameEditForm(instance=game)
    else:
        form = GameEditForm(request.POST, request.FILES, instance=game)
        if form.is_valid():
            form.save()  # user stays the same
            return redirect('index')
        else:
            print(form.errors)

    context = {'form': form, 'game': game}
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
