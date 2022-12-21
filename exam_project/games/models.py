from enum import Enum

from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models

UserModel = get_user_model()


class Choices(Enum):
    @classmethod
    def choices(cls):
        return [(x.name, x.value) for x in cls]

    @classmethod
    def max_len(cls):
        return max(len(name) for name, _ in cls.choices())


class Category(Choices):
    ACTION = "Action"
    ADVENTURE = "Adventure"
    PUZZLE = "Puzzle"
    STRATEGY = "Strategy"
    SPORTS = "Sports"
    BOARD = "Board/Card Game"
    OTHER = "Other"


class GameModel(models.Model):
    title = models.CharField(max_length=30, unique=True, null=False, blank=False, )
    category = models.CharField(max_length=Category.max_len(), choices=Category.choices(), )
    price = models.IntegerField(null=False, blank=False, validators=(validators.MinValueValidator(10),), )
    image_url = models.URLField(null=True, blank=True, )
    summary = models.TextField(null=True, blank=True, )
    user = models.ForeignKey(UserModel, default=None, on_delete=models.CASCADE, )

    def __str__(self):
        return f'{self.title}  --  {self.category}'


# class GameComment(models.Model):
#     text = models.CharField(max_length=400, null=False, blank=False,)
#     publication_date_time = models.DateTimeField(auto_now_add=True, null=False, blank=True,)
#     user = models.ForeignKey(user_model, default=None, on_delete=models.RESTRICT, )
