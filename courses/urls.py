from django.urls import path

from . import views


app_name = 'courses'

urlpatterns = [
    path('summer-2018/', views.Summer2018.as_view(), name='summer-2018'),
    path('dgs/', views.DGSSignup.as_view(), name='dgs'),
    path('dgs/<id>/payment/', views.DGSPayment.as_view(), name='dgs-payment'),
]
