from django.urls import path, re_path

from . import api, views


app_name = 'events'

urlpatterns = [
    path('', views.EventList.as_view(), name='event-list'),
    path('<pk>/', views.BookEvent.as_view(), name='book-event'),
]

range_api_urlpatterns = [
    path('', api.date_list, name='date-list'),
    re_path('^(?P<date>\d{4}-\d{2}-\d{2})/$', api.date_slots, name='date-slots'),
]
