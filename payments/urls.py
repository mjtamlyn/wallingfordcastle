from django.urls import path

from . import views

app_name = 'payments'

urlpatterns = [
    path('', views.StripeWebhook.as_view(), name='webhook'),
]
