from django.contrib.auth import get_user_model
from django.db import models
from exam_project.games.models import GameModel

UserModel = get_user_model()


class BoughtGame(models.Model):
    game = models.ForeignKey(
        GameModel,
        on_delete=models.CASCADE,
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = ('game', 'user')
