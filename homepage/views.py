from datetime import datetime, timedelta
from django.shortcuts import render
from django.template import RequestContext
import api


def index(request):
    uid = request.COOKIES.get("uid")
    data = None
    if not uid:
        uid, _ = api.create_new_user()
    else:
        data = api.get_saved_cities(uid)

    response = render(
        request,
        "homepage/index.html",
        {"saved_cities": data}
    )

    expires = datetime.utcnow() + timedelta(days=180)
    response.set_cookie("uid", uid, expires=expires)

    return response
