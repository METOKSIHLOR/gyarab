# @csrf_exempt - oprava chyb CSRF.
# V produkčním prostředí se to nedoporučuje,
# ale protože se jedná o studijní projekt, bylo rozhodnuto ponechat to tak, jak je.

import uuid

from django import forms
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from core.storage import storage
from game.models import Score
from users.auth.hash import hash_password, verify_password
from users.models import User
from utils import check_method, check_data, get_user_profile

# forma pro registrace a login
class UserCredsForm(forms.Form):
    name = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)

@csrf_exempt
def user_register(request):
    """Funkce registruje nového uživatele."""
    check_method(request, "POST")
    data = check_data(request)

    if isinstance(data, JsonResponse):
        return data

    form = UserCredsForm(data)

    if form.is_valid():
        username = form.cleaned_data['name']
        hashed_password = hash_password(form.cleaned_data["password"])

        if User.objects.filter(name=username).exists():
            return JsonResponse({"error": "Username already exists"}, status=409)

        user = User.objects.create(name=username, hashed_password=hashed_password)
        return JsonResponse({"status": "success"})

    return JsonResponse(form.errors, status=400)

@csrf_exempt
def user_login(request):
    """Authorizace uživatele."""
    check_method(request, "POST")
    data = check_data(request)

    if isinstance(data, JsonResponse):
        return data

    form = UserCredsForm(data)
    if form.is_valid():
        username = form.cleaned_data['name']
        password = form.cleaned_data["password"]
        user = User.objects.filter(name=username).first()
        if user and verify_password(password=password, hashed=user.hashed_password):
            session_id = str(uuid.uuid4()) # randomní řetěz symbolů pro session id
            storage.set(name=f"session_id:{session_id}", value=user.id, ex=3600) # session id do redis schranky
            response = JsonResponse({"status": "success"})

            response.set_cookie(
                key="session_id",
                value=session_id,
                httponly=True, # aby nikdo nemohl čist tu Cookie pomoci JS
                samesite='Lax' # obrana od CSRF utoků
            )

            return response
        return JsonResponse({"error": "Invalid username or password"}, status=401)

    return JsonResponse(form.errors, status=400)


@csrf_exempt
def user_logout(request):
    """Logout uživatele."""
    check_method(request, "DELETE")
    session_id = request.COOKIES.get("session_id")

    if not session_id or storage.delete(f"session_id:{session_id}") == 0: # jestli neni session id v cookie nebo nic se neodtranilo z redis
        return JsonResponse({"error": "User not authorized"}, status=403)

    response = JsonResponse({"status": "success", "message": "Logged out"})

    response.delete_cookie("session_id")

    return response

@csrf_exempt
# dostat profile uživatele
def user_profile(request):
    check_method(request, "GET")
    try:
        profile = get_user_profile(request)
    except ValueError as e:
        error_data = e.args[0]
        return JsonResponse({"error": error_data["error"]}, status=error_data["status"])
    return JsonResponse({"name": profile.name,
                         "points": profile.score.points,
                         "pps": profile.points_per_second,
                         "ppc": profile.points_per_click})


# Tyto funkce se používame k zobrazení HTML souborů pomocí Djanga.
def register_render(request):
    try:
        user = get_user_profile(request)
    except ValueError as e:
        return render(request, "register/register.html")
    return redirect("../game") # pokud uživatel už je authorizovan

def login_render(request):
    try:
        user = get_user_profile(request)
    except ValueError as e:
        return render(request, "login/login.html")
    return redirect("../game") # pokud uživatel už je authorizovan
