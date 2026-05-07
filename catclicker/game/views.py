from django import forms
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from game.models import Score
from users.models import UserUpgrade
from utils import get_user_profile, check_method, check_data

upgrades = [
    {"name": "cat mint", "cost": 1, "effect": {"pps": 1, "ppc": 0}},
    {"name": "ball of thread", "cost": 100, "effect": {"pps": 0, "ppc": 1}},
    {"name": "scratching post", "cost": 300, "effect": {"pps": 3, "ppc": 1}},
    {"name": "cat bed", "cost": 500, "effect": {"pps": 3, "ppc": 3}},
    {"name": "cat hat", "cost": 1000, "effect": {"pps": 7, "ppc": 7}},
]

class UpdateForm(forms.Form):
    name = forms.CharField(max_length=100)

@csrf_exempt
def click_cat(request):
    check_method(request, method="POST")
    try:
        user = get_user_profile(request)
    except ValueError as e:
        error_data = e.args[0]
        return JsonResponse({"error": error_data["error"]}, status=error_data["status"])

    with transaction.atomic():
        score = Score.objects.select_for_update().get(user=user)

        score.update_points()

        score.points += user.points_per_click

        score.save()

    return JsonResponse({"points": score.points})

@csrf_exempt
def buy_upgrade(request):
    check_method(request, method="POST")
    data = check_data(request)

    form = UpdateForm(data)
    if not form.is_valid():
        return JsonResponse(form.errors, status=400)

    body = form.cleaned_data
    try:
        user = get_user_profile(request)
    except ValueError as e:
        error_data = e.args[0]
        return JsonResponse({"error": error_data["error"]}, status=error_data["status"])

    upgrade = next((u for u in upgrades if u["name"] == body["name"]), None)
    if not upgrade:
        return HttpResponse("Upgrade not found", status=404)

    try:
        with transaction.atomic():
            score = Score.objects.select_for_update().get(user=user)

            score.update_points()

            if score.points < upgrade["cost"]:
                return HttpResponse("Not enough points", status=403)

            score.points -= upgrade["cost"]
            score.save()

            obj, created = UserUpgrade.objects.get_or_create(
                user=user,
                upgrade_name=body["name"]
            )
            obj.quantity += 1
            obj.save()

            user.points_per_second += upgrade["effect"]["pps"]
            user.points_per_click += upgrade["effect"]["ppc"]
            user.save()

    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)

    return HttpResponse(f"You bought {body['name']}. Total points: {score.points}")

def game_render(request):
    try:
        get_user_profile(request)
    except ValueError as e:
        return redirect("../login/")
    return render(request, "game/game.html")


