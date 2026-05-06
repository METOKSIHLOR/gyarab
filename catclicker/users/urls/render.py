from django.contrib import admin
from django.urls import path

from users.views import register_render, login_render

urlpatterns = [
    path("login/", login_render),
    path("register/", register_render),
]