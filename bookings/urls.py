from django.urls import path

from . import views

app_name = 'bookings'


urlpatterns = [
    path('', views.BookingsIndex.as_view(), name='index'),
]
