from django.urls import path

from game.views import game_render

urlpatterns = [
    path("game/", game_render)
]
