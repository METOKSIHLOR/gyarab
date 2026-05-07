"""Tento soubor obsahuje všechny pomocné funkce, které jsou vyžadovány v několika aplikacích současně."""

import json
from typing import Literal

from django.http import Http404, JsonResponse

from core.storage import storage
from users.models import User


def check_method(request, method: Literal["POST", "PUT", "DELETE", "PATCH", "GET"]):
    """Funkce kontroluje, zda požadavek obsahuje metodu požadovanou pro koncový bod, jinak vrátí chybu 404."""
    if request.method != method:
        raise Http404("Page not found")

def check_data(request):
    """Funkce kontroluje, zda je tělo požadavku v platném formátu JSON."""
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    return data

def get_user_profile(request):
    """Moje magnum opus. Bastl a hvězda celého backendu.
     Vrací chybu, pokud uživatel není autorizován, ale vyžaduje neustálé try/except pro zpracování této chyby."""
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