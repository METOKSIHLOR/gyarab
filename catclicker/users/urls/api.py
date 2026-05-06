from django.contrib import admin
from django.urls import path

from users.views import user_register, user_login, user_profile, user_logout

urlpatterns = [
    path("register/", user_register),
    path("login/", user_login),
    path("logout/", user_logout),
    path("profile/", user_profile)
]
