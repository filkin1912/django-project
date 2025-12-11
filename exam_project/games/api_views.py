from rest_framework import generics, permissions, filters, status
from rest_framework.response import Response
from django.db import transaction
from .models import GameModel
from exam_project.common.models import BoughtGame
from .serializers import GameSerializer, GameUpdateSerializer, BoughtGameSerializer


class GamesListCreateApiView(generics.ListCreateAPIView):
    queryset = GameModel.objects.select_related('user').all()
    serializer_class = GameSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title']
    ordering_fields = ['price', 'title', 'id']
    ordering = ['-id']

    def perform_create(self, serializer):
        # Debug print to see which user is creating the game
        print("Creating game for user:", self.request.user)
        serializer.save(user=self.request.user)


class GameRetrieveUpdateDeleteApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = GameModel.objects.select_related('user').all()

    def get_permissions(self):
        if self.request.method in ('PATCH', 'PUT', 'DELETE'):
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def check_object_permissions(self, request, obj):
        if request.method in ('PATCH', 'PUT', 'DELETE') and obj.user_id != request.user.id:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You can only modify your own listings.")
        return super().check_object_permissions(request, obj)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GameSerializer
        return GameUpdateSerializer


class MyGamesListApiView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GameSerializer

    def get_queryset(self):
        return GameModel.objects.filter(user=self.request.user).select_related('user')


class GameBuyApiView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BoughtGameSerializer

    def post(self, request, *args, **kwargs):
        game_id = kwargs['pk']
        buyer = request.user

        with transaction.atomic():
            try:
                game = GameModel.objects.select_for_update().get(pk=game_id)
            except GameModel.DoesNotExist:
                return Response({"detail": "Game not found."}, status=status.HTTP_404_NOT_FOUND)

            seller = game.user

            if BoughtGame.objects.filter(user=buyer, game=game).exists():
                return Response({"detail": "Already purchased."}, status=status.HTTP_400_BAD_REQUEST)

            if buyer.money < game.price:
                return Response({"detail": "Insufficient funds."}, status=status.HTTP_400_BAD_REQUEST)

            # Deduct from buyer
            buyer.money -= game.price
            buyer.save(update_fields=['money'])

            # Credit seller
            seller.money += game.price
            seller.save(update_fields=['money'])

            # Create purchase record
            bg = BoughtGame.objects.create(user=buyer, game=game)

        return Response({"id": bg.id, "game": game.id}, status=status.HTTP_201_CREATED)
