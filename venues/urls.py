from django.urls import path

from . import views


app_name = 'venues'


urlpatterns = [
    path('', views.Venues.as_view(), name='index'),
]
