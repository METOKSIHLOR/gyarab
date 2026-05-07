from django.urls import path

from game.views import click_cat, buy_upgrade

urlpatterns = [
    path("click/", click_cat),
    path("upgrade/", buy_upgrade),
]
