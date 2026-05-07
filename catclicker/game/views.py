# @csrf_exempt - oprava chyb CSRF.
# V produkčním prostředí se to nedoporučuje,
# ale protože se jedná o studijní projekt, bylo rozhodnuto ponechat to tak, jak je.

from django import forms
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from game.models import Score
from users.models import UserUpgrade
from utils import get_user_profile, check_method, check_data

# Seznam dostupných vylepšení s jejich cenou a efektem
upgrades = [
    {"name": "cat mint", "cost": 1, "effect": {"pps": 1, "ppc": 0}},
    {"name": "ball of thread", "cost": 100, "effect": {"pps": 0, "ppc": 1}},
    {"name": "scratching post", "cost": 300, "effect": {"pps": 3, "ppc": 1}},
    {"name": "cat bed", "cost": 500, "effect": {"pps": 3, "ppc": 3}},
    {"name": "cat hat", "cost": 1000, "effect": {"pps": 7, "ppc": 7}},
]

# Jednoduchý formulář pro validaci názvu vylepšení při nákupu
class UpdateForm(forms.Form):
    name = forms.CharField(max_length=100)

@csrf_exempt
def update_points(request):
    """Aktualizuje body na základě uplynulého času (pasivní příjem)."""
    check_method(request, method="POST")

    try:
        user = get_user_profile(request)
    except ValueError as e:
        error_data = e.args[0]
        return JsonResponse({"error": error_data["error"]}, status=error_data["status"])

    # Použití transakce a locku (select_for_update), aby se předešlo race condition
    with transaction.atomic():
        score = Score.objects.select_for_update().get(user=user)
        score.update_points() # Výpočet bodů za dobu, kdy byl uživatel offline
        score.save()

    return JsonResponse({"points": score.points})

@csrf_exempt
def click_cat(request):
    """Zpracuje kliknutí na kočku: přičte pasivní body a body za klik."""
    check_method(request, method="POST")
    try:
        user = get_user_profile(request)
    except ValueError as e:
        error_data = e.args[0]
        return JsonResponse({"error": error_data["error"]}, status=error_data["status"])

    with transaction.atomic():
        score = Score.objects.select_for_update().get(user=user)
        score.update_points() # Nejdříve dopočítáme pasivní příjem
        score.points += user.points_per_click # Přičteme body za aktuální kliknutí
        score.save()

    return JsonResponse({"points": score.points})

@csrf_exempt
def buy_upgrade(request):
    """Logika nákupu vylepšení: kontrola zůstatku a aktualizace statistik uživatele."""
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

    # Vyhledání vylepšení v seznamu podle názvu
    upgrade = next((u for u in upgrades if u["name"] == body["name"]), None)
    if not upgrade:
        return HttpResponse("Upgrade not found", status=404)

    try:
        with transaction.atomic():
            score = Score.objects.select_for_update().get(user=user)
            score.update_points() # Aktualizace bodů před kontrolou zůstatku

            if score.points < upgrade["cost"]:
                return HttpResponse("Not enough points", status=403)

            # Odečtení ceny a uložení záznamu o nákupu
            score.points -= upgrade["cost"]
            score.save()

            obj, created = UserUpgrade.objects.get_or_create(
                user=user,
                upgrade_name=body["name"]
            )
            obj.quantity += 1
            obj.save()

            # Zlepšení statistik uživatele (PPS - body za sekundu, PPC - body za klik)
            user.points_per_second += upgrade["effect"]["pps"]
            user.points_per_click += upgrade["effect"]["ppc"]
            user.save()

    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)

    return HttpResponse(f"You bought {body['name']}. Total points: {score.points}")

def game_render(request):
    """Renderování hlavní herní stránky s kontrolou autorizace."""
    try:
        get_user_profile(request) # Pokud profil neexistuje (uživatel není přihlášen), vyvolá chybu
    except ValueError as e:
        return redirect("../login/") # Redirect na login pro neautorizované uživatele
    return render(request, "game/game.html")
