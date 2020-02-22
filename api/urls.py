from django.urls import path

from . import views

urlpatterns = (
    path('weather/', views.weather, name='api-weather'),
    path('city/add/', views.city_add, name='api-city-add'),
    path('city/remove/', views.city_remove, name='api-city-remove'),
)
