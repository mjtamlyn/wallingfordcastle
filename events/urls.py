from django.urls import path, register_converter

from . import api, views
from .converters import ApiDateConverter, SlotReferenceConverter

app_name = 'events'

register_converter(ApiDateConverter, 'date')
register_converter(SlotReferenceConverter, 'slot')

urlpatterns = [
    path('', views.EventList.as_view(), name='event-list'),
    path('<pk>/', views.BookEvent.as_view(), name='book-event'),
]

range_api_urlpatterns = [
    path('', api.date_list, name='date-list'),
    path('<date:date>/', api.date_slots, name='date-slots'),
    path('archers/', api.bookable_archers, name='bookable-archers'),
    path('absentable-archers/<slot:slot>', api.slot_absentable_archers, name='slot-absentable-archers'),
    path('book/', api.book_slot, name='book-slot'),
    path('cancel/', api.cancel_slot, name='cancel-slot'),
]
