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
