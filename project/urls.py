from django.conf.urls import patterns, include, url

# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r"^$",    include("homepage.urls")),
    url(r"^api/", include("api.urls")),
)
