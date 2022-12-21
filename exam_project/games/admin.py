from django.contrib import admin

from exam_project.games.models import GameModel


@admin.register(GameModel)
class GameModelAdmin(admin.ModelAdmin):
    pass
