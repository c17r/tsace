import json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
import api


def weather(request):
    name = request.GET.get("name")
    lat = request.GET.get("lat")
    lng = request.GET.get("lng")

    if not name or not lat or not lng:
        return HttpResponseBadRequest()

    data = api.get_weather(lat, lng, name)
    return HttpResponse(json.dumps(data), content_type="application/json")


def city_add(request):
    key = request.POST.get("key")
    uid = request.COOKIES.get("uid")

    if not key or not uid:
        return HttpResponseBadRequest()

    api.add_city_to_user(uid, key)
    return HttpResponse()


def city_remove(request):
    key = request.POST.get("key")
    uid = request.COOKIES.get("uid")

    if not key or not uid:
        return HttpResponseBadRequest()

    api.remove_city_from_user(uid, key)
    return HttpResponse()
