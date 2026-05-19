from django.urls import path

from game.views import click_cat, buy_upgrade, update_points, get_upgrades

urlpatterns = [
    path("click/", click_cat),
    path("upgrade/", buy_upgrade),
    path("upgrades/", get_upgrades),
    path("update_points/", update_points)
]
