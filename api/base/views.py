import json

import django.http as http
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from base.helpers import create_json_response
import django.contrib.auth as django_auth


@csrf_exempt
@require_POST
def login(request):
    username = request.POST.get("username", "")
    password = request.POST.get("password", "")

    user = django_auth.authenticate(
        request, username=username, password=password)

    if user is not None:
        django_auth.login(request, user)

        return create_json_response()
    else:
        return create_json_response(
            success=False,
            message="Login failed",
        )


def logout(request):
    django_auth.logout(request)

    return create_json_response()


@csrf_exempt
@require_POST
def register(request):
    username = request.POST.get("username", "")
    password = request.POST.get("password", "")

    if username and password:
        django_auth.models.User.objects.create_user(
            username=username,
            password=password,
        )

        return create_json_response()
    else:
        return create_json_response(
            success=False,
            message="Missing username or password",
            status=400
        )
