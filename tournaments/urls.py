from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.TournamentHome.as_view(), name='home'),
    url(r'^enter/$', views.EntryCreate.as_view(), name='enter'),
    url(r'^entry/(?P<pk>\d+)/$', views.EntryUpdate.as_view(), name='entry-update'),
    url(r'^enter/(?P<pk>\d+)/delete/$', views.EntryDelete.as_view(), name='entry-delete'),
    url(r'^pay/$', views.Pay.as_view(), name='pay'),
]
