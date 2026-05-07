import json
from typing import Literal

from django.http import Http404, JsonResponse

from core.storage import storage
from users.models import User


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