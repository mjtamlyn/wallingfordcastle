from django.urls import re_path

from . import views


app_name = 'membership'

urlpatterns = [
    re_path('^$', views.Overview.as_view(), name='overview'),
    re_path('^update/(?P<member_id>\d+)/$', views.MemberUpdate.as_view(), name='member-update'),
    re_path('^payment/$', views.PaymentDetails.as_view(), name='payment-details'),
]
