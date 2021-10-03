from django.urls import path

from . import views


app_name = 'venues'


urlpatterns = [
    path('', views.VenueList.as_view(), name='index'),
    path('<slug:slug>/', views.VenueDetail.as_view(), name='detail'),
]
