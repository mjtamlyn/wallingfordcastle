from django.urls import path, re_path

from . import views

app_name = 'membership'

urlpatterns = [
    path('', views.Overview.as_view(), name='overview'),
    re_path(r'^range/', views.RangeBooking.as_view(), name='range-booking'),
    path('attendance/<member_id>/', views.MemberAttendance.as_view(), name='member-attendance'),
    path('update/<member_id>/', views.MemberUpdate.as_view(), name='member-update'),
    path('payment/', views.PaymentDetails.as_view(), name='payment-details'),
]
