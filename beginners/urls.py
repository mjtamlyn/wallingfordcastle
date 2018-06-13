from django.urls import path

from . import views


app_name = 'beginners'

urlpatterns = [
    path('', views.BeginnersIndex.as_view(), name='index'),
    path('beginners/', views.BeginnersInterestView.as_view(), name='interest'),
    path('payment/', views.Payment.as_view(), name='payment'),
]
