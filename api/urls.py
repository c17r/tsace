from django.conf.urls import patterns, url
from views import WeatherView, CityView

urlpatterns = patterns(
    "",

    url(r"^weather/(?P<name>[^/]+)/(?P<lat>[\-\d\.]+),(?P<lng>[\-\d\.]+)/$",
        WeatherView.as_view(),
        name="weather"),

    url(r"^city/?(?P<key>[^/]+)?/$",
        CityView.as_view(),
        name="city"),
)
