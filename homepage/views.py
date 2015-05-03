from datetime import datetime, timedelta
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
import api


class HomepageView(TemplateView):

    template_name = "homepage/index.html"

    @method_decorator(ensure_csrf_cookie)
    def get(self, request, *args, **kwargs):
        response = super(HomepageView, self).get(request, *args, **kwargs)

        uid = request.COOKIES.get("uid")
        if not uid:
            uid, _ = api.create_new_user()
        expires = datetime.utcnow() + timedelta(days=180)
        response.set_cookie("uid", uid, expires=expires)

        return response
