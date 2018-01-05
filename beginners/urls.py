from django.conf.urls import re_path

from . import views


app_name = 'beginners'

urlpatterns = [
    re_path(r'^beginners/$', views.BeginnersInterestView.as_view(), name='interest'),
    re_path(r'^payment/$', views.Payment.as_view(), name='payment'),
]
