from django.conf.urls import url

from . import views


urlpatterns = [
    url('^$', views.Overview.as_view(), name='overview'),
]
