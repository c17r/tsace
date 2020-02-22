from django.urls import include, path

from homepage.views import index as homepage

urlpatterns = (
    path('', homepage, name='homepage'),
    path('api/', include('api.urls')),
)
