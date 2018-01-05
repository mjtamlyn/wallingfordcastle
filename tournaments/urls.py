from django.conf.urls import re_path

from . import views

app_name = 'tournaments'

urlpatterns = [
    re_path(r'^$', views.TournamentHome.as_view(), name='home'),
    re_path(r'^register/$', views.TournamentRegistration.as_view(), name='register'),
    re_path(r'^enter/$', views.EntryCreate.as_view(), name='enter'),
    re_path(r'^entry/(?P<pk>\d+)/$', views.EntryUpdate.as_view(), name='entry-update'),
    re_path(r'^enter/(?P<pk>\d+)/delete/$', views.EntryDelete.as_view(), name='entry-delete'),
    re_path(r'^pay/$', views.Pay.as_view(), name='pay'),
]
