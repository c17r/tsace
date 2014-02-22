from django.conf.urls import patterns, url

urlpatterns = patterns(
    "",
    url(r"^weather/$", "api.views.weather", name="api-weather"),
    url(r"^city/add/$", "api.views.city_add", name="api-city-add"),
    url(r"^city/remove/$", "api.views.city_remove", name="api-city-remove"),
)
