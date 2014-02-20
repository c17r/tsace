import json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from api.models import ForecastIO


def weather(request):
    name = request.GET.get("name")
    lat = request.GET.get("lat")
    lng = request.GET.get("lng")

    if not name or not lat or not lng:
        return HttpResponseBadRequest()

    data = ForecastIO.get_weather(lat, lng)
    return HttpResponse(json.dumps(data), content_type="application/json")