from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^beginners/$', views.BeginnersInterestView.as_view(), name='interest'),
    url(r'^payment/$', views.Payment.as_view(), name='payment'),
]
