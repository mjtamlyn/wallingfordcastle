from django.urls import path

from . import views


app_name = 'courses'

urlpatterns = [
    path('dgs/', views.DGSSignup.as_view(), name='dgs'),
    path('dgs/payment/', views.DGSPayment.as_view(), name='dgs-payment'),
]
