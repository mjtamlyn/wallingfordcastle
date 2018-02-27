from django.urls import path

from . import views


app_name = 'events'

urlpatterns = [
    path('', views.EventList.as_view(), name='event-list'),
    path('<pk>/', views.BookEvent.as_view(), name='book-event'),
]
