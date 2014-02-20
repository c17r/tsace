from django.conf.urls import patterns, url

urlpatterns = patterns(
    "",
    url(r"^weather/$", "api.views.weather", name="api-weather")
)
