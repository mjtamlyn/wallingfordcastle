from django.urls import path

from . import views


app_name = 'coaching'

urlpatterns = [
    path('', views.GroupsOverview.as_view(), name='overview'),
]
