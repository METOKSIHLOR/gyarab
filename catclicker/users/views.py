import json
import uuid
from typing import Literal

from django import forms
from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from core.storage import storage
from game.models import Score
from users.auth.hash import hash_password, verify_password
from users.models import User


class UserCredsForm(forms.Form):
    name = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)

def check_method(request, method: Literal["POST", "PUT", "DELETE", "PATCH", "GET"]):
    if request.method != method:
        raise Http404("Page not found")

def check_data(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    return data

def get_user_profile(request):
    session_id = request.COOKIES.get("session_id")

    if not session_id:
        raise ValueError({"error": "User not authorized",
                                  "status": 401})

    user_id = storage.get(name=f"session_id:{session_id}")

    if not user_id:
        raise ValueError({"error": "Session expired or invalid",
                          "status": 401})
    user = User.objects.filter(id=user_id).first()

    if not user:
        raise ValueError({"error": "User not found",
                          "status": 404})
    return user

@csrf_exempt
def user_register(request):
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
            session_id = str(uuid.uuid4())
            storage.set(name=f"session_id:{session_id}", value=user.id, ex=3600)
            response = JsonResponse({"status": "success"})
            response.set_cookie(
                key="session_id",
                value=session_id,
                httponly=True,
                samesite='Lax'
            )
            return response
        return JsonResponse({"error": "Invalid username or password"}, status=401)

    return JsonResponse(form.errors, status=400)


@csrf_exempt
def user_logout(request):
    check_method(request, "DELETE")
    session_id = request.COOKIES.get("session_id")

    if not session_id or storage.delete(f"session_id:{session_id}") == 0:
        return JsonResponse({"error": "User not authorized"}, status=403)

    response = JsonResponse({"status": "success", "message": "Logged out"})

    response.delete_cookie("session_id")

    return response

@csrf_exempt
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

def register_render(request):
    return HttpResponse("Hello, world. You're at the register page.")
    #return render(request, "users/register.html")

def login_render(request):
    return HttpResponse("Hello, world. You're at the login page.")
    #return render(request, "users/login.html")
