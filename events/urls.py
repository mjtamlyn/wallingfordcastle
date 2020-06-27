from django.urls import path

from . import api, views


app_name = 'events'

urlpatterns = [
    path('', views.EventList.as_view(), name='event-list'),
    path('<pk>/', views.BookEvent.as_view(), name='book-event'),
]

range_api_urlpatterns = [
    path('', api.date_list, name='date-list'),
]
