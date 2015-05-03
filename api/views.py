import json
from django.views.decorators.csrf import ensure_csrf_cookie
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.generic import View
import api


class WeatherView(View):

    def get(self, request, *args, **kwargs):
        name = kwargs["name"]
        lat = kwargs["lat"]
        lng = kwargs["lng"]

        data = api.get_weather(lat, lng, name)
        return HttpResponse(json.dumps(data), content_type="application/json")


class CityView(View):

    def dispatch(self, request, *args, **kwargs):
        uid = request.COOKIES.get("uid")
        if not uid:
            raise PermissionDenied
        kwargs['uid'] = uid
        return super(CityView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        uid = kwargs['uid']

        data = api.get_saved_cities(uid)
        return HttpResponse(json.dumps(data), content_type="application/json")

    def put(self, request, *args, **kwargs):
        key = kwargs['key']
        uid = kwargs['uid']

        success, _ = api.add_city_to_user(uid, key)
        if not success:
            return HttpResponseBadRequest()
        data = api.get_saved_cities(uid)
        return HttpResponse(json.dumps(data), content_type="application/json")

    def delete(self, request, *args, **kwargs):
        key = kwargs['key']
        uid = kwargs['uid']

        success, _ = api.remove_city_from_user(uid, key)
        if not success:
            return HttpResponseBadRequest()
        data = api.get_saved_cities(uid)
        return HttpResponse(json.dumps(data), content_type="application/json")
