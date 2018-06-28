from django.urls import path

from . import views


app_name = 'courses'

urlpatterns = [
    path('summer-2018/', views.Summer2018.as_view(), name='summer-2018'),
    path('summer-2018/book/', views.Summer2018Book.as_view(), name='summer-2018-book'),
    path('summer-2018/<id>/payment/', views.Summer2018Payment.as_view(), name='summer-2018-payment'),
    path('dgs/', views.DGSSignup.as_view(), name='dgs'),
    path('dgs/<id>/payment/', views.DGSPayment.as_view(), name='dgs-payment'),
]
