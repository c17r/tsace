from django.conf.urls import patterns, include, url

# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r"^$", 'homepage.views.index', name="homepage"),
    url(r"^api/", include("api.urls")),
)
