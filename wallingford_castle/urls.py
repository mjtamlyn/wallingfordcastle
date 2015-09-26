from django.conf.urls import patterns, include, url
from django.contrib import admin

from . import views


urlpatterns = patterns('',
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^membership-interest/$', views.MembershipInterestView.as_view(), name='membership-interest'),
    url(r'^beginners-course/$', views.BeginnersCourseView.as_view(), name='beginners-course'),

    url(r'^members/', include('membership.urls', namespace='membership')),
    url(r'^admin/', include(admin.site.urls)),
)
