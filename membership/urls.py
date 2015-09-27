from django.conf.urls import url

from . import views


urlpatterns = [
    url('^$', views.Overview.as_view(), name='overview'),
    url('^update/(?P<member_id>\d+)/$', views.MemberUpdate.as_view(), name='member-update'),
]
